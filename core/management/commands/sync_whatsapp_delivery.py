from django.core.management.base import BaseCommand

from core.integrations import credentials_ready, message_status
from core.models import DeliveryLog


class Command(BaseCommand):
    help = 'Refresh pending WhatsApp delivery statuses using Twilio message IDs.'

    def handle(self, *args, **options):
        if not credentials_ready():
            self.stdout.write('Provider credentials missing.')
            return
        for record in DeliveryLog.objects.filter(status__in=[
                'pending', 'accepted', 'queued', 'sending', 'sent']).exclude(provider_id='')[:200]:
            try:
                result = message_status(record.provider_id)
                record.status = result.get('status', record.status)
                record.error = str(result.get('error_message') or '')[:300]
                record.save(update_fields=['status', 'error'])
            except ValueError:
                self.stderr.write(f'Could not update log #{record.pk}.')
        self.stdout.write('Delivery statuses updated.')
