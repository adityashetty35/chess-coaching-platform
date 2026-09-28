from django.contrib import admin
from .models import FeePlan, Invoice, Payment, PaymentReminder

@admin.register(FeePlan)
class FeePlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'frequency', 'is_active')
    list_filter = ('frequency', 'is_active')
    search_fields = ('name', 'description')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'description', 'amount', 'amount_paid', 'due_date', 'status')
    list_filter = ('status', 'due_date', 'fee_plan')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'description')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'payment_date', 'method')
    list_filter = ('method', 'payment_date')
    search_fields = ('invoice__student__user__first_name', 'invoice__student__user__last_name', 'reference')

@admin.register(PaymentReminder)
class PaymentReminderAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'scheduled_date', 'reminder_type', 'status', 'sent_at')
    list_filter = ('status', 'reminder_type', 'scheduled_date')
    search_fields = ('invoice__student__user__first_name', 'invoice__student__user__last_name', 'message')
