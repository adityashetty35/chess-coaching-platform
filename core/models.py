import json

from django.db import models

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
