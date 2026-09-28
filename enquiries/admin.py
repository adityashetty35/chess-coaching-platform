from django.contrib import admin
from .models import Enquiry, EnquiryFollowUp

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('student_name', 'phone', 'email')

@admin.register(EnquiryFollowUp)
class EnquiryFollowUpAdmin(admin.ModelAdmin):
    list_display = ('enquiry', 'created_at', 'next_follow_up')
    list_filter = ('created_at', 'next_follow_up')
