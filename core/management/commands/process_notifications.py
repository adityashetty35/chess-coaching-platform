from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run fee reminder schedules, then refresh WhatsApp message delivery statuses.'

    def handle(self, *args, **options):
        call_command('send_fee_reminders', stdout=self.stdout, stderr=self.stderr)
        call_command('sync_whatsapp_delivery', stdout=self.stdout, stderr=self.stderr)
