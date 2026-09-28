from django.urls import path
from . import views

app_name = "coaching"

urlpatterns = [
    # Batches
    path("batches/", views.batch_list, name="batch_list"),
    path("batches/add/", views.batch_form, name="batch_add"),
    path("batches/<int:pk>/edit/", views.batch_form, name="batch_edit"),
    path("batches/<int:pk>/delete/", views.batch_delete, name="batch_delete"),
    # Classes
    path("", views.class_list, name="class_list"),
    path("add/", views.class_form, name="class_add"),
    path("<int:pk>/", views.class_detail, name="class_detail"),
    path("<int:pk>/edit/", views.class_form, name="class_edit"),
    path("<int:pk>/delete/", views.class_delete, name="class_delete"),
    path("<int:pk>/attendance/", views.mark_attendance, name="mark_attendance"),
    # Calendar
    path("calendar/", views.calendar_view, name="calendar"),
    path("calendar/events/", views.calendar_events, name="calendar_events"),
]
