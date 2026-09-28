from django.contrib import admin
from .models import ProgressEntry, Goal

@admin.register(ProgressEntry)
class ProgressEntryAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'rating')
    list_filter = ('date', 'student')
    search_fields = ('student__first_name', 'student__last_name')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'status', 'priority', 'target_date')
    list_filter = ('status', 'priority', 'target_date')
    search_fields = ('title', 'student__first_name', 'student__last_name')
