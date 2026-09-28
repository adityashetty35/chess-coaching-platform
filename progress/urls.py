from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('student/<int:student_pk>/', views.progress_list, name='list'),
    path('student/<int:student_pk>/add/', views.progress_form, name='form'),
    path('student/<int:student_pk>/<int:pk>/edit/', views.progress_form, name='form'),
    path('student/<int:student_pk>/<int:pk>/delete/', views.progress_delete, name='delete'),
    
    path('student/<int:student_pk>/goals/', views.goal_list, name='goal_list'),
    path('student/<int:student_pk>/goals/add/', views.goal_form, name='goal_form'),
    path('student/<int:student_pk>/goals/<int:pk>/edit/', views.goal_form, name='goal_form'),
    path('student/<int:student_pk>/goals/<int:pk>/delete/', views.goal_delete, name='goal_delete'),
]
