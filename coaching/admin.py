from django.contrib import admin
from .models import Batch, ChessClass, Attendance

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'mode', 'is_active', 'created_at')
    list_filter = ('level', 'mode', 'is_active')
    search_fields = ('name',)

@admin.register(ChessClass)
class ChessClassAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'class_type', 'date', 'start_time', 'status')
    list_filter = ('class_type', 'mode', 'status', 'date')
    search_fields = ('title', 'topic')
    filter_horizontal = ('students',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'chess_class', 'status', 'marked_at')
    list_filter = ('status', 'marked_at')
    search_fields = ('student__first_name', 'student__last_name', 'chess_class__title')
