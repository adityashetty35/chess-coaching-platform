from django.urls import path
from . import views

app_name = 'assignments'

urlpatterns = [
    path('', views.assignment_list, name='list'),
    path('add/', views.assignment_form, name='form'),
    path('<int:pk>/', views.assignment_detail, name='detail'),
    path('<int:pk>/edit/', views.assignment_form, name='form'),
    path('<int:pk>/delete/', views.assignment_delete, name='delete'),
    path('<int:pk>/submission/<int:submission_pk>/update/', views.update_submission_status, name='update_submission'),
]
