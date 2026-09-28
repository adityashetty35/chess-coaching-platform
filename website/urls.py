from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("enquiry/", views.enquiry_form, name="enquiry"),
    path("enquiry/thank-you/", views.enquiry_thank_you, name="enquiry_thank_you"),
]
