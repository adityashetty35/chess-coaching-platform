from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.announcement_list, name='list'),
    path('add/', views.announcement_form, name='form'),
    path('<int:pk>/', views.announcement_detail, name='detail'),
    path('<int:pk>/edit/', views.announcement_form, name='form'),
    path('<int:pk>/delete/', views.announcement_delete, name='delete'),
]
