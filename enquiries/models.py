from django.db import models

class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('trial_scheduled', 'Trial Scheduled'),
        ('interested', 'Interested'),
        ('converted', 'Converted'),
        ('not_interested', 'Not Interested'),
        ('follow_up', 'Follow Up Later'),
    ]

    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('both', 'Both'),
    ]

    LEVEL_CHOICES = [
        ('absolute_beginner', 'Absolute Beginner'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('tournament', 'Tournament Player'),
    ]

    student_name = models.CharField(max_length=200)
    parent_name = models.CharField(max_length=200, blank=True, default='')
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(blank=True, default='')

    current_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    current_rating = models.PositiveIntegerField(blank=True, null=True,
                                                  help_text='FIDE/online rating if available')
    preferred_mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='both')
    preferred_schedule = models.TextField(blank=True, default='',
                                          help_text='Preferred days and times')
    coaching_goal = models.TextField(blank=True, default='')
    message = models.TextField(blank=True, default='')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=100, blank=True, default='website')
    notes = models.TextField(blank=True, default='')
    follow_up_date = models.DateField(blank=True, null=True)

    converted_student = models.ForeignKey(
        'students.Student', on_delete=models.SET_NULL,
        blank=True, null=True, related_name='source_enquiry'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f"{self.student_name} - {self.get_status_display()}"


class EnquiryFollowUp(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='follow_ups')
    notes = models.TextField()
    next_follow_up = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Follow-up for {self.enquiry.student_name} on {self.created_at.strftime('%Y-%m-%d')}"
