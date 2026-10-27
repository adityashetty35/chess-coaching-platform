from datetime import date, time, timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.core.management import call_command
from django.utils import timezone
from django.urls import reverse

from coaching.models import ChessClass
from core.models import AuditLog, IntegrationSettings, UserRole, WhatsAppTemplate, ReminderSchedule, DeliveryLog
from students.models import Parent, Student
from fees.models import FeePlan, Invoice


class AcademyAccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser('owner', 'owner@example.com', 'SafeTestPass#123')
        self.admin = User.objects.create_user('admin', password='SafeTestPass#123', is_staff=True)
        UserRole.objects.create(user=self.admin, role=UserRole.ACADEMY_ADMIN, permissions=['students', 'dashboard'])
        self.coach = User.objects.create_user('trainer', password='SafeTestPass#123', is_staff=True)
        UserRole.objects.create(user=self.coach, role=UserRole.COACH)
        self.parent_user = User.objects.create_user('guardian', password='SafeTestPass#123')
        UserRole.objects.create(user=self.parent_user, role=UserRole.PARENT)
        self.student = Student.objects.create(first_name='Alice', joining_date=date.today())
        self.parent = Parent.objects.create(user=self.parent_user, name='Guardian', phone='+919876543210')
        self.parent.students.add(self.student)
        self.assigned = ChessClass.objects.create(date=date.today(), start_time=time(10), end_time=time(11),
                                                  assigned_coach=self.coach)
        self.unassigned = ChessClass.objects.create(date=date.today(), start_time=time(12), end_time=time(13))

    def test_super_admin_can_manage_users(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(reverse('administration:users')).status_code, 200)

    def test_only_owner_manages_integration_and_roles(self):
        for person in (self.admin, self.coach, self.parent_user):
            self.client.force_login(person)
            self.assertEqual(self.client.get(reverse('administration:integrations')).status_code, 403)
            self.assertEqual(self.client.get(reverse('administration:users')).status_code, 403)

    def test_admin_permissions_enforced_server_side(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('students:list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('fees:invoice_list')).status_code, 403)
        self.assertEqual(self.client.get(reverse('settings:index')).status_code, 403)

    def test_coach_sees_only_assigned_class(self):
        self.client.force_login(self.coach)
        self.assertEqual(self.client.get(reverse('coaching:class_detail', args=[self.assigned.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('coaching:class_detail', args=[self.unassigned.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse('coaching:class_add')).status_code, 403)
        self.assertEqual(self.client.get(reverse('students:list')).status_code, 403)

    def test_parent_sees_portal_only(self):
        self.client.force_login(self.parent_user)
        self.assertEqual(self.client.get(reverse('portal:dashboard')).status_code, 200)
        self.assertRedirects(self.client.get(reverse('students:list')), reverse('portal:dashboard'))

    def test_permission_changes_are_audited(self):
        self.client.force_login(self.owner)
        data = {'username': 'admin', 'first_name': 'A', 'last_name': '', 'email': '',
                'is_active': 'on', 'role': UserRole.ACADEMY_ADMIN, 'permissions': ['dashboard']}
        response = self.client.post(reverse('administration:user_edit', args=[self.admin.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserRole.objects.get(user=self.admin).permissions, ['dashboard'])
        self.assertTrue(AuditLog.objects.filter(action='user_permissions_changed', actor=self.owner).exists())

    def test_cannot_demote_self(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse('administration:user_edit', args=[self.owner.pk]), {
            'username': 'owner', 'role': UserRole.ACADEMY_ADMIN, 'is_active': 'on'})
        self.assertEqual(response.status_code, 200)
        self.owner.refresh_from_db()
        self.assertTrue(self.owner.is_superuser)

    def test_fee_changes_are_audited(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse('fees:plan_add'), {
            'name': 'Monthly lessons', 'description': '', 'amount': '1500.00',
            'frequency': 'monthly', 'is_active': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FeePlan.objects.filter(name='Monthly lessons').exists())
        self.assertTrue(AuditLog.objects.filter(action='fee_record_created', actor=self.owner).exists())

    def test_integration_update_audited_without_credentials(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(reverse('administration:integrations')).status_code, 200)
        response = self.client.post(reverse('administration:integrations'), {
            'whatsapp_provider': 'disabled', 'sms_provider': 'disabled',
            'reminder_days_before': 2, 'otp_cooldown_seconds': 60, 'otp_max_attempts': 5,
            'whatsapp_template': 'Please pay {amount}.'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(AuditLog.objects.filter(action='integration_settings_changed').exists())

    def test_template_and_schedule_forms_render(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(reverse('administration:template_new')).status_code, 200)
        self.assertEqual(self.client.get(reverse('administration:schedule_new')).status_code, 200)
        response = self.client.post(reverse('administration:template_new'), {
            'name': 'Fee reminder', 'content_sid': 'HX' + '2' * 32,
            'preview_text': 'Fees due for {student_name}.', 'is_active': 'on'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WhatsAppTemplate.objects.filter(name='Fee reminder').exists())

    @patch('core.management.commands.send_fee_reminders.send_whatsapp', return_value={
        'sid': 'SMtest123', 'status': 'queued'})
    @patch('core.management.commands.send_fee_reminders.credentials_ready', return_value=True)
    def test_scheduled_whatsapp_is_idempotent(self, ready, send):
        config = IntegrationSettings.load()
        config.whatsapp_provider = 'twilio'
        config.whatsapp_sender = '+14155238886'
        config.reminders_enabled = True
        config.save()
        template = WhatsAppTemplate.objects.create(name='Fee due', content_sid='HX' + '1' * 32)
        ReminderSchedule.objects.create(name='Two days before', days_offset=-2, template=template)
        self.parent.whatsapp = '+919876543210'
        self.parent.save()
        Invoice.objects.create(student=self.student, description='Monthly tuition', amount='1000.00',
                               due_date=timezone.localdate() + timedelta(days=2))
        call_command('send_fee_reminders')
        call_command('send_fee_reminders')
        send.assert_called_once()
        self.assertEqual(DeliveryLog.objects.count(), 1)

    @patch('core.otp_views.start_verification')
    @patch('core.otp_views.verify_ready', return_value=True)
    def test_parent_otp_flow(self, ready, send):
        config = IntegrationSettings.load()
        config.parent_otp_enabled = True
        config.sms_provider = 'twilio_verify'
        config.save()
        response = self.client.post(reverse('accounts:otp_login'), {'phone': '+919876543210'})
        self.assertRedirects(response, reverse('accounts:otp_verify'))
        send.assert_called_once()
        with patch('core.otp_views.check_verification', return_value={'status': 'approved'}):
            response = self.client.post(reverse('accounts:otp_verify'), {'code': '123456'})
        self.assertRedirects(response, reverse('portal:dashboard'))
