from django.urls import path
from . import views

app_name = "settings"

urlpatterns = [
    path("", views.settings_view, name="index"),
    path("services/", views.services_list, name="services"),
    path("services/add/", views.service_form, name="service_add"),
    path("services/<int:pk>/edit/", views.service_form, name="service_edit"),
    path("services/<int:pk>/delete/", views.service_delete, name="service_delete"),
    path("programs/", views.programs_list, name="programs"),
    path("programs/add/", views.program_form, name="program_add"),
    path("programs/<int:pk>/edit/", views.program_form, name="program_edit"),
    path("programs/<int:pk>/delete/", views.program_delete, name="program_delete"),
    path("testimonials/", views.testimonials_list, name="testimonials"),
    path("testimonials/add/", views.testimonial_form, name="testimonial_add"),
    path("testimonials/<int:pk>/edit/", views.testimonial_form, name="testimonial_edit"),
    path("testimonials/<int:pk>/delete/", views.testimonial_delete, name="testimonial_delete"),
    path("faqs/", views.faqs_list, name="faqs"),
    path("faqs/add/", views.faq_form, name="faq_add"),
    path("faqs/<int:pk>/edit/", views.faq_form, name="faq_edit"),
    path("faqs/<int:pk>/delete/", views.faq_delete, name="faq_delete"),
    path("achievements/", views.achievements_list, name="achievements"),
    path("achievements/add/", views.achievement_form, name="achievement_add"),
    path("achievements/<int:pk>/edit/", views.achievement_form, name="achievement_edit"),
    path("achievements/<int:pk>/delete/", views.achievement_delete, name="achievement_delete"),
]
