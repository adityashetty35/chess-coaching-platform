from django.urls import path
from . import views

app_name = "fees"

urlpatterns = [
    # Fee Plans
    path("plans/", views.fee_plan_list, name="plan_list"),
    path("plans/add/", views.fee_plan_form, name="plan_add"),
    path("plans/<int:pk>/edit/", views.fee_plan_form, name="plan_edit"),
    path("plans/<int:pk>/delete/", views.fee_plan_delete, name="plan_delete"),
    # Invoices
    path("", views.invoice_list, name="invoice_list"),
    path("add/", views.invoice_form, name="invoice_add"),
    path("<int:pk>/", views.invoice_detail, name="invoice_detail"),
    path("<int:pk>/edit/", views.invoice_form, name="invoice_edit"),
    path("<int:pk>/delete/", views.invoice_delete, name="invoice_delete"),
    # Payments
    path("<int:invoice_pk>/pay/", views.record_payment, name="record_payment"),
    path("payments/", views.payment_list, name="payment_list"),
    # Reminders
    path("reminders/", views.reminder_list, name="reminder_list"),
    path("<int:invoice_pk>/remind/", views.create_reminder, name="create_reminder"),
    path("reminders/<int:pk>/cancel/", views.cancel_reminder, name="cancel_reminder"),
    path("<int:invoice_pk>/whatsapp-reminder/", views.whatsapp_reminder, name="whatsapp_reminder"),
]
