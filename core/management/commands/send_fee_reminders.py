from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.db.models import F
from django.utils import timezone

from core.integrations import credentials_ready, send_whatsapp
from core.models import DeliveryLog, IntegrationSettings, ReminderSchedule
from fees.models import Invoice, PaymentReminder


class Command(BaseCommand):
    help = 'Send scheduled WhatsApp fee reminders through the configured approved Twilio template.'

    def handle(self, *args, **options):
        config = IntegrationSettings.load()
        if not (config.reminders_enabled and config.whatsapp_provider == 'twilio'
                and credentials_ready() and config.whatsapp_sender):
            self.stdout.write('WhatsApp reminders disabled or provider not configured.')
            return
        today = timezone.localdate()
        schedules = list(ReminderSchedule.objects.select_related('template'))
        rules = [(rule.days_offset, rule.template, f'fee_reminder_{rule.pk}')
                 for rule in schedules if rule.is_active and (not rule.template or rule.template.is_active)]
        if not schedules:
            rules = [(-config.reminder_days_before, None, 'fee_reminder')]
        for offset, template, message_type in rules:
            due_on = today - timedelta(days=offset)
            invoices = Invoice.objects.filter(due_date=due_on).exclude(status='cancelled').filter(
                amount__gt=F('amount_paid')).select_related('student')
            for invoice in invoices:
                self.send_one(invoice, config, template, message_type, today)
        self.stdout.write('Reminder run completed.')

    def send_one(self, invoice, config, template, message_type, today):
        parent = invoice.student.parents.filter(preferred_communication='whatsapp').exclude(whatsapp='').first()
        if not parent:
            return
        phone = '+' + ''.join(ch for ch in parent.whatsapp if ch.isdigit())
        if len(phone) < 9 or len(phone) > 16:
            return
        try:
            with transaction.atomic():
                log, created = DeliveryLog.objects.get_or_create(
                    invoice=invoice, scheduled_for=today, message_type=message_type,
                    defaults={'recipient': phone, 'status': 'pending'})
                if not created:
                    return
        except IntegrityError:
            return
        try:
            preview = (template.preview_text if template else config.whatsapp_template).format(
                parent_name=parent.name, student_name=invoice.student.full_name,
                amount=invoice.balance, due_date=invoice.due_date.strftime('%d %b %Y'))
            response = send_whatsapp(phone, {
                '1': parent.name, '2': invoice.student.full_name,
                '3': str(invoice.balance), '4': invoice.due_date.strftime('%d %b %Y'),
            }, config, content_sid=template.content_sid if template else None)
            log.status = response.get('status', 'accepted')
            log.provider_id = response.get('sid', '')
            PaymentReminder.objects.create(
                invoice=invoice, reminder_type='whatsapp', scheduled_date=today,
                message=preview,
                status='pending', notes='Submitted to WhatsApp provider; delivery not confirmed.')
        except (ValueError, KeyError) as exc:
            log.status = 'failed'
            log.error = str(exc)[:300]
        finally:
            log.save(update_fields=['status', 'provider_id', 'error'])
