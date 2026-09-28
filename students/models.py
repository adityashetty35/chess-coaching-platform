from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    LEVEL_CHOICES = [
        ('absolute_beginner', 'Absolute Beginner'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('tournament', 'Tournament Player'),
    ]

    COACHING_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
        ('both', 'Both'),
    ]

    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('both', 'Both'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_break', 'On Break'),
        ('graduated', 'Graduated'),
    ]

    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='student_profile')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, default='')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, default='',
                              choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    photo = models.ImageField(upload_to='students/', blank=True, null=True)

    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    whatsapp = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')

    school = models.CharField(max_length=200, blank=True, default='')
    school_class = models.CharField(max_length=50, blank=True, default='', verbose_name='Class/Grade')

    joining_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    coaching_type = models.CharField(max_length=15, choices=COACHING_TYPE_CHOICES, default='individual')
    preferred_mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='offline')
    batch = models.ForeignKey('coaching.Batch', on_delete=models.SET_NULL,
                              blank=True, null=True, related_name='students')

    chess_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    fide_id = models.CharField(max_length=50, blank=True, default='', verbose_name='FIDE ID')
    fide_rating = models.PositiveIntegerField(blank=True, null=True, verbose_name='FIDE Rating')
    chess_com_username = models.CharField(max_length=100, blank=True, default='', verbose_name='Chess.com Username')
    lichess_username = models.CharField(max_length=100, blank=True, default='', verbose_name='Lichess Username')

    strengths = models.TextField(blank=True, default='')
    weaknesses = models.TextField(blank=True, default='')
    chess_goals = models.TextField(blank=True, default='')
    preferred_openings = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class Parent(models.Model):
    RELATIONSHIP_CHOICES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
        ('other', 'Other'),
    ]

    COMMUNICATION_CHOICES = [
        ('phone', 'Phone Call'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
    ]

    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='parent_profile')

    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=15, choices=RELATIONSHIP_CHOICES, default='father')
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    preferred_communication = models.CharField(max_length=10, choices=COMMUNICATION_CHOICES,
                                                default='whatsapp')
    students = models.ManyToManyField(Student, related_name='parents', blank=True)
    notes = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
