from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.portal_dashboard, name="dashboard"),
    path("classes/", views.portal_classes, name="classes"),
    path("attendance/", views.portal_attendance, name="attendance"),
    path("homework/", views.portal_homework, name="homework"),
    path("progress/", views.portal_progress, name="progress"),
    path("learning/", views.portal_learning, name="learning"),
    path("fees/", views.portal_fees, name="fees"),
]
