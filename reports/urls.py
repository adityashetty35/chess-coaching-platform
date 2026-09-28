from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.reports_index, name="index"),
    path("fees/", views.fees_report, name="fees"),
    path("students/", views.students_report, name="students"),
    path("attendance/", views.attendance_report, name="attendance"),
    path("enquiries/", views.enquiries_report, name="enquiries"),
    path("export/<str:report_type>/", views.export_csv, name="export_csv"),
]
