import json

from django.db import models
from django.conf import settings


class UserRole(models.Model):
    SUPER_ADMIN = 'super_admin'
    ACADEMY_ADMIN = 'academy_admin'
    COACH = 'coach'
    PARENT = 'parent'
    ROLE_CHOICES = [(SUPER_ADMIN, 'Super Administrator'), (ACADEMY_ADMIN, 'Academy Admin'),
                    (COACH, 'Coach'), (PARENT, 'Parent')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='academy_role')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=PARENT)
    permissions = models.JSONField(default=list, blank=True, help_text='Enabled Academy Admin modules')

    def __str__(self):
        return f'{self.user.username} — {self.get_role_display()}'


class IntegrationSettings(models.Model):
    WHATSAPP_CHOICES = [('disabled', 'Disabled'), ('twilio', 'Twilio WhatsApp')]
    SMS_CHOICES = [('disabled', 'Disabled'), ('twilio_verify', 'Twilio Verify')]
    whatsapp_provider = models.CharField(max_length=24, choices=WHATSAPP_CHOICES, default='disabled')
    whatsapp_sender = models.CharField(max_length=32, blank=True, default='', help_text='Twilio approved WhatsApp sender, e.g. +14155238886')
    whatsapp_content_sid = models.CharField(max_length=50, blank=True, default='', help_text='Approved Twilio Content template SID for business-initiated reminders')
    whatsapp_template = models.TextField(default='Hello {parent_name}, fees of {amount} for {student_name} are due on {due_date}.')
    reminder_days_before = models.PositiveSmallIntegerField(default=3)
    reminders_enabled = models.BooleanField(default=False)
    sms_provider = models.CharField(max_length=24, choices=SMS_CHOICES, default='disabled')
    parent_otp_enabled = models.BooleanField(default=False)
    otp_cooldown_seconds = models.PositiveSmallIntegerField(default=60)
    otp_max_attempts = models.PositiveSmallIntegerField(default=5)

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]

    def save(self, *args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)


class WhatsAppTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content_sid = models.CharField(max_length=50, help_text='Twilio-approved WhatsApp Content SID')
    preview_text = models.TextField(default='Hello {parent_name}, fees of {amount} for {student_name} are due on {due_date}.')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ReminderSchedule(models.Model):
    name = models.CharField(max_length=100)
    days_offset = models.SmallIntegerField(default=-3, help_text='Days relative to due date: -3 is 3 days before; 0 is on due date; 2 is 2 days after.')
    template = models.ForeignKey(WhatsAppTemplate, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['days_offset', 'id']

    def __str__(self):
        return self.name


class DeliveryLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.CharField(max_length=32)
    message_type = models.CharField(max_length=32, default='fee_reminder')
    invoice = models.ForeignKey('fees.Invoice', null=True, blank=True, on_delete=models.SET_NULL)
    scheduled_for = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    provider_id = models.CharField(max_length=100, blank=True, default='')
    error = models.CharField(max_length=300, blank=True, default='')

    class Meta:
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['invoice', 'message_type', 'scheduled_for'],
                                               name='unique_reminder_delivery_per_date')]


class OTPRequest(models.Model):
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    consumed = models.BooleanField(default=False)


class AuditLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    target = models.CharField(max_length=160)
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class SiteSettings(models.Model):
    academy_name = models.CharField(max_length=200, default='Chess Academy')
    coach_name = models.CharField(max_length=200, default='Coach')
    logo = models.ImageField(upload_to='branding/', blank=True, null=True)
    favicon = models.ImageField(upload_to='branding/', blank=True, null=True)
    about = models.TextField(blank=True, default='')
    tagline = models.CharField(max_length=300, blank=True, default='Master the Game of Kings')

    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    whatsapp = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')

    website_url = models.URLField(blank=True, default='')
    facebook_url = models.URLField(blank=True, default='')
    instagram_url = models.URLField(blank=True, default='')
    youtube_url = models.URLField(blank=True, default='')
    twitter_url = models.URLField(blank=True, default='')
    linkedin_url = models.URLField(blank=True, default='')

    currency_symbol = models.CharField(max_length=5, default='₹')
    currency_code = models.CharField(max_length=5, default='INR')

    fee_reminder_template = models.TextField(
        blank=True,
        default='Hello {parent_name}, this is a friendly reminder that the chess coaching fee of ₹{amount} for {student_name} is pending. Due date: {due_date}. Thank you.'
    )

    hero_title = models.CharField(max_length=300, blank=True, default='Elevate Your Chess Game')
    hero_subtitle = models.TextField(blank=True, default='Expert coaching for players of all levels. From beginners to tournament champions.')
    hero_cta_text = models.CharField(max_length=100, blank=True, default='Book a Free Trial')

    coach_title = models.CharField(max_length=200, blank=True, default='FIDE Rated Coach')
    coach_photo = models.ImageField(upload_to='branding/', blank=True, null=True)
    coach_bio = models.TextField(blank=True, default='')
    coach_experience = models.CharField(max_length=200, blank=True, default='10+ Years Experience')
    coach_rating = models.CharField(max_length=100, blank=True, default='')
    coach_students_trained = models.CharField(max_length=100, blank=True, default='500+')

    how_it_works = models.TextField(blank=True, default='',
                                     help_text='JSON list of steps: [{"title":"...", "description":"..."}]')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.academy_name

    @property
    def whatsapp_digits(self):
        # wa.me links only accept digits, e.g. "+91 98765-43210" -> "919876543210"
        return ''.join(ch for ch in self.whatsapp if ch.isdigit())

    @property
    def how_it_works_steps(self):
        try:
            steps = json.loads(self.how_it_works or '[]')
        except ValueError:
            return []
        return [s for s in steps if isinstance(s, dict) and s.get('title')]

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class CoachingService(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, default='bi-trophy',
                            help_text='Bootstrap icon class')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class CoachingProgram(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    features = models.TextField(blank=True, default='',
                                help_text='One feature per line')
    price_label = models.CharField(max_length=100, blank=True, default='',
                                   help_text='e.g. "₹3000/month" or "Contact for pricing"')
    is_popular = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, blank=True, default='Student',
                            help_text='e.g. Student, Parent, Tournament Player')
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"


class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class Achievement(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, default='')
    date = models.DateField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, default='bi-award')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date']

    def __str__(self):
        return self.title
