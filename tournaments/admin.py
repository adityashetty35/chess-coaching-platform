from django.contrib import admin
from .models import TournamentResult

@admin.register(TournamentResult)
class TournamentResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'tournament_name', 'date', 'score')
    list_filter = ('date',)
    search_fields = ('tournament_name', 'student__first_name', 'student__last_name')
