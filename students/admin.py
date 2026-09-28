from django.contrib import admin
from .models import Student, Parent

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'status', 'chess_level')
    list_filter = ('status', 'chess_level', 'coaching_type')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'phone', 'email')
    list_filter = ('relationship', 'preferred_communication')
    search_fields = ('name', 'phone', 'email')
