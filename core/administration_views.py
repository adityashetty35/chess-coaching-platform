import os
from functools import wraps

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .admin_forms import IntegrationForm, ManagedUserForm, WhatsAppTemplateForm, ReminderScheduleForm
from .integrations import credentials_ready, verify_ready
from .models import AuditLog, DeliveryLog, IntegrationSettings, UserRole, WhatsAppTemplate, ReminderSchedule
from students.models import Parent


def super_admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied()
        return view(request, *args, **kwargs)
    return wrapped


@super_admin_required
def users(request):
    records = get_user_model().objects.all().order_by('username').select_related('academy_role')
    return render(request, 'core/admin_users.html', {'records': records})


@super_admin_required
@transaction.atomic
def user_form(request, pk=None):
    instance = get_object_or_404(get_user_model(), pk=pk) if pk else None
    form = ManagedUserForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        selected_role = form.cleaned_data['role']
        if instance == request.user and selected_role != UserRole.SUPER_ADMIN:
            form.add_error('role', 'You cannot remove your own Super Administrator role.')
        else:
            old = UserRole.objects.filter(user=instance).first() if instance else None
            before = {'role': old.role, 'permissions': old.permissions} if old else {}
            user = form.save(commit=False)
            user.is_superuser = selected_role == UserRole.SUPER_ADMIN
            user.is_staff = selected_role != UserRole.PARENT
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])
            user.save()
            perms = form.cleaned_data['permissions'] if selected_role == UserRole.ACADEMY_ADMIN else []
            UserRole.objects.update_or_create(user=user, defaults={'role': selected_role, 'permissions': perms})
            if selected_role == UserRole.PARENT:
                target_parent = form.cleaned_data.get('parent_profile')
                if target_parent:
                    Parent.objects.filter(user=user).exclude(pk=target_parent.pk).update(user=None)
                    target_parent.user = user
                    target_parent.save(update_fields=['user'])
            AuditLog.objects.create(actor=request.user, action='user_permissions_changed', target=user.username,
                                    details={'before': before, 'after': {'role': selected_role, 'permissions': perms}})
            messages.success(request, 'User and permissions saved.')
            return redirect('administration:users')
    return render(request, 'core/admin_user_form.html', {'form': form, 'editing': bool(pk)})


@super_admin_required
def integrations(request):
    config = IntegrationSettings.load()
    form = IntegrationForm(request.POST or None, instance=config)
    if request.method == 'POST' and form.is_valid():
        before = {key: getattr(config, key) for key in form.cleaned_data}
        updated = form.save()
        after = {key: getattr(updated, key) for key in form.cleaned_data}
        AuditLog.objects.create(actor=request.user, action='integration_settings_changed',
                                target='Twilio / OTP configuration', details={'before': before, 'after': after})
        messages.success(request, 'Integration settings saved. Provider credentials remain in server environment variables.')
        return redirect('administration:integrations')
    return render(request, 'core/admin_integrations.html', {
        'form': form, 'whatsapp_ready': credentials_ready(), 'otp_ready': verify_ready(),
        'credentials': ('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_VERIFY_SERVICE_SID'),
        'templates': WhatsAppTemplate.objects.all().order_by('name'),
        'schedules': ReminderSchedule.objects.select_related('template').all(),
    })


@super_admin_required
def template_form(request, pk=None):
    instance = get_object_or_404(WhatsAppTemplate, pk=pk) if pk else None
    form = WhatsAppTemplateForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        previous = {'name': instance.name, 'content_sid': instance.content_sid} if instance else None
        item = form.save()
        AuditLog.objects.create(actor=request.user, action='whatsapp_template_changed', target=item.name,
                                details={'before': previous, 'after': {'name': item.name, 'content_sid': item.content_sid}})
        messages.success(request, 'WhatsApp template saved.')
        return redirect('administration:integrations')
    return render(request, 'core/admin_integration_form.html', {
        'form': form, 'title': 'WhatsApp template', 'help': 'Create the approved content in Twilio first, then enter its Content SID here.'})


@super_admin_required
def schedule_form(request, pk=None):
    instance = get_object_or_404(ReminderSchedule, pk=pk) if pk else None
    form = ReminderScheduleForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        previous = {'days_offset': instance.days_offset, 'is_active': instance.is_active} if instance else None
        item = form.save()
        AuditLog.objects.create(actor=request.user, action='reminder_schedule_changed', target=item.name,
                                details={'before': previous, 'after': {'days_offset': item.days_offset, 'is_active': item.is_active}})
        messages.success(request, 'Reminder schedule saved.')
        return redirect('administration:integrations')
    return render(request, 'core/admin_integration_form.html', {
        'form': form, 'title': 'Reminder schedule', 'help': 'Negative days are before the fee due date; positive days are after.'})


@super_admin_required
def deliveries(request):
    return render(request, 'core/admin_deliveries.html', {'records': DeliveryLog.objects.all()[:150]})


@super_admin_required
def audit(request):
    return render(request, 'core/admin_audit.html', {'records': AuditLog.objects.select_related('actor')[:200]})
