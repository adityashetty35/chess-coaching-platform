from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='list'),
    path('add/', views.student_form, name='add'),
    path('<int:student_id>/', views.student_detail, name='detail'),
    path('<int:student_id>/edit/', views.student_form, name='edit'),
    path('<int:student_id>/delete/', views.student_delete, name='delete'),
    path('<int:student_id>/create-login/', views.create_student_login, name='create_login'),
    
    path('parents/', views.parent_list, name='parent_list'),
    path('parents/add/', views.parent_form, name='parent_add'),
    path('parents/<int:parent_id>/edit/', views.parent_form, name='parent_edit'),
    path('parents/<int:parent_id>/delete/', views.parent_delete, name='parent_delete'),
    path('parents/<int:parent_id>/create-login/', views.create_parent_login, name='parent_create_login'),
]
