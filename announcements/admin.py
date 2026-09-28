from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'priority', 'is_active', 'publish_date')
    list_filter = ('audience', 'priority', 'is_active')
    search_fields = ('title',)
