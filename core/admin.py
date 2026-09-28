from django.contrib import admin
from .models import SiteSettings, CoachingService, CoachingProgram, Testimonial, FAQ, Achievement

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Academy Info', {'fields': ('academy_name', 'coach_name', 'logo', 'tagline', 'about')}),
        ('Contact', {'fields': ('email', 'phone', 'whatsapp', 'address')}),
        ('Social Media', {'fields': ('website_url', 'facebook_url', 'instagram_url',
                                      'youtube_url', 'twitter_url', 'linkedin_url')}),
        ('Currency', {'fields': ('currency_symbol', 'currency_code')}),
        ('Fee Reminders', {'fields': ('fee_reminder_template',)}),
        ('Website Hero', {'fields': ('hero_title', 'hero_subtitle', 'hero_cta_text')}),
        ('Coach Profile', {'fields': ('coach_title', 'coach_photo', 'coach_bio',
                                       'coach_experience', 'coach_rating', 'coach_students_trained')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(CoachingService)
class CoachingServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(CoachingProgram)
class CoachingProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_label', 'is_popular', 'order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'rating', 'is_active']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'is_active']
