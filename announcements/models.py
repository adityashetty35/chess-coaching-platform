from django.db import models

class Announcement(models.Model):
    AUDIENCE_CHOICES = [
        ('everyone', 'Everyone'),
        ('students', 'All Students'),
        ('parents', 'All Parents'),
        ('batch', 'Specific Batch'),
        ('individual', 'Specific Students'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=300)
    content = models.TextField()
    audience = models.CharField(max_length=15, choices=AUDIENCE_CHOICES, default='everyone')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')

    batch = models.ForeignKey('coaching.Batch', on_delete=models.SET_NULL,
                              blank=True, null=True, related_name='announcements')
    students = models.ManyToManyField('students.Student', blank=True,
                                      related_name='announcements')

    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title
