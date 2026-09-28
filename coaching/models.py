from django.db import models

class Batch(models.Model):
    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('mixed', 'Mixed'),
    ]

    name = models.CharField(max_length=200)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='offline')
    schedule = models.TextField(blank=True, default='',
                                help_text='e.g. Mon/Wed/Fri 4:00-5:00 PM')
    max_students = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Batches'

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    @property
    def student_count(self):
        return self.students.filter(status='active').count()


class ChessClass(models.Model):
    CLASS_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
    ]

    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]

    title = models.CharField(max_length=200, blank=True, default='')
    class_type = models.CharField(max_length=15, choices=CLASS_TYPE_CHOICES, default='individual')
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='offline')

    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL,
                              blank=True, null=True, related_name='classes')
    students = models.ManyToManyField('students.Student', blank=True, related_name='classes')

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    topic = models.CharField(max_length=500, blank=True, default='')
    description = models.TextField(blank=True, default='')
    homework = models.TextField(blank=True, default='')
    coach_notes = models.TextField(blank=True, default='')

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        label = self.title or self.topic or f"{self.get_class_type_display()} Class"
        return f"{label} - {self.date}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    chess_class = models.ForeignKey(ChessClass, on_delete=models.CASCADE,
                                     related_name='attendance_records')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE,
                                related_name='attendance_records')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    notes = models.CharField(max_length=300, blank=True, default='')
    marked_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['chess_class', 'student']
        ordering = ['-chess_class__date']

    def __str__(self):
        return f"{self.student} - {self.chess_class.date} - {self.get_status_display()}"
