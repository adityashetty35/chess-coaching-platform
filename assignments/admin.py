from django.contrib import admin
from .models import Assignment, AssignmentSubmission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'batch')
    list_filter = ('due_date', 'batch')
    search_fields = ('title',)

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'status')
    list_filter = ('status',)
    search_fields = ('assignment__title', 'student__first_name', 'student__last_name')
