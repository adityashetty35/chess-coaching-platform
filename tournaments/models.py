from django.db import models

class TournamentResult(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE,
                                related_name='tournament_results')
    tournament_name = models.CharField(max_length=300)
    date = models.DateField()
    location = models.CharField(max_length=200, blank=True, default='')

    total_rounds = models.PositiveIntegerField(blank=True, null=True)
    score = models.CharField(max_length=20, blank=True, default='')
    rank = models.PositiveIntegerField(blank=True, null=True)
    total_participants = models.PositiveIntegerField(blank=True, null=True)

    rating_before = models.PositiveIntegerField(blank=True, null=True)
    rating_after = models.PositiveIntegerField(blank=True, null=True)
    performance_rating = models.PositiveIntegerField(blank=True, null=True)

    highlights = models.TextField(blank=True, default='')
    coach_notes = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.tournament_name}"

    @property
    def rating_change(self):
        if self.rating_before and self.rating_after:
            return self.rating_after - self.rating_before
        return None
