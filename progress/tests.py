from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve, Resolver404
from students.models import Student, Parent
from .models import SyllabusLesson, TestResult, FideRatingRecord, ScheduledTest
from fees.models import Invoice
from enquiries.models import Enquiry


class AcademyScopeTests(TestCase):
    def setUp(self):
        self.coach = User.objects.create_user(username='coach', password='testpass', is_staff=True)
        self.parent_user = User.objects.create_user(username='parent', password='testpass')
        self.other_user = User.objects.create_user(username='other', password='testpass')
        self.mine = Student.objects.create(first_name='My child', joining_date=date.today())
        self.other = Student.objects.create(first_name='Other child', joining_date=date.today())
        Parent.objects.create(user=self.parent_user, name='Parent One', phone='1234567890').students.add(self.mine)
        Parent.objects.create(user=self.other_user, name='Parent Two', phone='1234567891').students.add(self.other)
        TestResult.objects.create(student=self.mine, title='My test', test_date=date.today(), score=8, max_score=10)
        TestResult.objects.create(student=self.other, title='Private test', test_date=date.today(), score=9, max_score=10)
        FideRatingRecord.objects.create(student=self.other, recorded_on=date.today(), rating=1200,
                                        source_url='https://ratings.fide.com/', verified_by=self.coach)
        SyllabusLesson.objects.create(level='foundation', title='Board fundamentals')

    def test_public_page_uses_academy_brief(self):
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Indian Chess Raider Academy')
        self.assertContains(response, '₹2,500')

    def test_parent_cannot_see_another_child_results(self):
        self.client.force_login(self.parent_user)
        response = self.client.get(reverse('portal:learning'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My test')
        self.assertNotContains(response, 'Private test')
        self.assertNotContains(response, '1200')

    def test_parent_cannot_edit_academy_records(self):
        self.client.force_login(self.parent_user)
        response = self.client.get(reverse('progress:academy_add', args=['test']))
        self.assertRedirects(response, reverse('portal:dashboard'))

    def test_extra_features_are_not_routed(self):
        for path in ['/tournaments/', '/announcements/', '/reports/']:
            with self.assertRaises(Resolver404):
                resolve(path)

    def test_dashboard_uses_live_database_values(self):
        Invoice.objects.create(student=self.mine, description='Monthly fee', amount=2500,
                               amount_paid=500, due_date=date.today(), status='partially_paid')
        Enquiry.objects.create(student_name='Real applicant', phone='9876543210', status='new')
        ScheduledTest.objects.create(title='Upcoming assessment', level='foundation', date=date.today())
        self.client.force_login(self.coach)
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['active_students'], 2)
        self.assertEqual(response.context['new_enquiries'], 1)
        self.assertEqual(response.context['pending_fees_total'], 2000)
        self.assertEqual(response.context['tests_recorded'], 2)
        self.assertContains(response, 'Upcoming assessment')
        self.assertContains(response, '₹2,000')
        self.assertNotContains(response, 'Sample data')

    def test_dashboard_without_records_displays_empty_states(self):
        ScheduledTest.objects.all().delete()
        self.client.force_login(self.coach)
        response = self.client.get(reverse('core:dashboard'))
        self.assertContains(response, 'No upcoming tests scheduled.')
        self.assertContains(response, 'No lessons scheduled.')
        self.assertContains(response, 'No enquiries recorded yet.')
