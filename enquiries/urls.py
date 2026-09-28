from django.urls import path
from . import views

app_name = "enquiries"

urlpatterns = [
    path("", views.enquiry_list, name="list"),
    path("<int:pk>/", views.enquiry_detail, name="detail"),
    path("add/", views.enquiry_form, name="add"),
    path("<int:pk>/edit/", views.enquiry_form, name="edit"),
    path("<int:pk>/status/", views.update_status, name="update_status"),
    path("<int:pk>/follow-up/", views.add_follow_up, name="add_follow_up"),
    path("<int:pk>/convert/", views.convert_to_student, name="convert"),
    path("<int:pk>/delete/", views.enquiry_delete, name="delete"),
]
