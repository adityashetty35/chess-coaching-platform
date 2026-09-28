from django.db import models

class ProgressEntry(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE,
                                related_name='progress_entries')
    date = models.DateField()

    rating = models.PositiveIntegerField(blank=True, null=True)
    tactics = models.PositiveIntegerField(blank=True, null=True)
    opening_knowledge = models.PositiveIntegerField(blank=True, null=True)
    middlegame = models.PositiveIntegerField(blank=True, null=True)
    endgame = models.PositiveIntegerField(blank=True, null=True)
    calculation = models.PositiveIntegerField(blank=True, null=True)
    positional = models.PositiveIntegerField(blank=True, null=True)
    time_management = models.PositiveIntegerField(blank=True, null=True)

    strengths = models.TextField(blank=True, default='')
    weaknesses = models.TextField(blank=True, default='')
    next_goals = models.TextField(blank=True, default='')
    coach_comments = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Progress Entry'
        verbose_name_plural = 'Progress Entries'

    def __str__(self):
        return f"{self.student} - {self.date}"


class Goal(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE,
                                related_name='goals')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, default='')
    target_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    progress_percent = models.PositiveIntegerField(default=0)
    coach_notes = models.TextField(blank=True, default='')
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student} - {self.title}"
