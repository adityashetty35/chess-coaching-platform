from django.db import models

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField()
    due_date = models.DateField()

    students = models.ManyToManyField('students.Student', blank=True,
                                      related_name='assignments')
    batch = models.ForeignKey('coaching.Batch', on_delete=models.SET_NULL,
                              blank=True, null=True, related_name='assignments')

    coach_notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('completed', 'Completed'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,
                                    related_name='submissions')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE,
                                related_name='assignment_submissions')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    student_notes = models.TextField(blank=True, default='')
    coach_feedback = models.TextField(blank=True, default='')
    completed_date = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['assignment', 'student']
        ordering = ['-assignment__due_date']

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
