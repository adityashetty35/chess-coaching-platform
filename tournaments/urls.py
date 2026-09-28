from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournament_list, name='list'),
    path('add/', views.tournament_form, name='add'),
    path('add/', views.tournament_form, name='form'),
    path('<int:pk>/edit/', views.tournament_form, name='edit'),
    path('<int:pk>/delete/', views.tournament_delete, name='delete'),
]
