from django.urls import path
from . import administration_views

app_name = 'administration'
urlpatterns = [
    path('users/', administration_views.users, name='users'),
    path('users/new/', administration_views.user_form, name='user_new'),
    path('users/<int:pk>/', administration_views.user_form, name='user_edit'),
    path('integrations/', administration_views.integrations, name='integrations'),
    path('templates/new/', administration_views.template_form, name='template_new'),
    path('templates/<int:pk>/', administration_views.template_form, name='template_edit'),
    path('schedules/new/', administration_views.schedule_form, name='schedule_new'),
    path('schedules/<int:pk>/', administration_views.schedule_form, name='schedule_edit'),
    path('deliveries/', administration_views.deliveries, name='deliveries'),
    path('audit/', administration_views.audit, name='audit'),
]
