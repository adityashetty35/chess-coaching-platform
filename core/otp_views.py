import re
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from students.models import Parent
from .integrations import check_verification, start_verification, verify_ready
from .models import IntegrationSettings, OTPRequest
from .permissions import role_for


def normalize_phone(value):
    raw = value.strip().replace(' ', '').replace('-', '')
    return raw if re.fullmatch(r'\+[1-9]\d{7,14}', raw) else None


@require_http_methods(['GET', 'POST'])
def otp_login(request):
    config = IntegrationSettings.load()
    if not config.parent_otp_enabled or config.sms_provider != 'twilio_verify' or not verify_ready():
        return render(request, 'registration/otp_unavailable.html', status=503)
    if request.method == 'POST':
        phone = normalize_phone(request.POST.get('phone', ''))
        if not phone:
            messages.error(request, 'Enter your phone with country code, e.g. +919876543210.')
        else:
            client = request.META.get('REMOTE_ADDR', 'unknown')
            key = f'otp_ip_{client}'
            if cache.get(key, 0) >= 10:
                messages.error(request, 'Too many attempts. Try again later.')
                return redirect('accounts:otp_login')
            cache.set(key, cache.get(key, 0) + 1, 3600)
            last = OTPRequest.objects.filter(phone=phone).order_by('-created_at').first()
            if last and timezone.now() - last.created_at < timedelta(seconds=config.otp_cooldown_seconds):
                messages.info(request, 'Please wait before requesting another code.')
                return redirect('accounts:otp_login')
            # Never let a shared number log in as an arbitrary parent.
            matched = [p for p in Parent.objects.filter(user__is_active=True).select_related('user')
                       if normalize_phone(p.phone) == phone and role_for(p.user) == 'parent']
            if len(matched) == 1:
                try:
                    start_verification(phone)
                except ValueError:
                    messages.error(request, 'Unable to send a code right now. Try again later.')
                    return redirect('accounts:otp_login')
                otp = OTPRequest.objects.create(phone=phone, user=matched[0].user)
                request.session['parent_otp_id'] = otp.id
                return redirect('accounts:otp_verify')
            messages.info(request, 'If that number is registered, a verification code will be sent.')
    return render(request, 'registration/otp_phone.html')


@require_http_methods(['GET', 'POST'])
def otp_verify(request):
    config = IntegrationSettings.load()
    if not config.parent_otp_enabled or config.sms_provider != 'twilio_verify' or not verify_ready():
        return render(request, 'registration/otp_unavailable.html', status=503)
    otp = OTPRequest.objects.filter(pk=request.session.get('parent_otp_id'), consumed=False).select_related('user').first()
    if not otp or timezone.now() - otp.created_at > timedelta(minutes=10) or otp.attempts >= config.otp_max_attempts:
        request.session.pop('parent_otp_id', None)
        messages.error(request, 'Your code expired. Request a new one.')
        return redirect('accounts:otp_login')
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        otp.attempts += 1
        otp.save(update_fields=['attempts'])
        if re.fullmatch(r'\d{4,10}', code):
            try:
                response = check_verification(otp.phone, code)
            except ValueError:
                response = {}
            if response.get('status') == 'approved' and otp.user.is_active and role_for(otp.user) == 'parent':
                otp.consumed = True
                otp.save(update_fields=['consumed'])
                request.session.pop('parent_otp_id', None)
                login(request, otp.user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('portal:dashboard')
        messages.error(request, 'Incorrect code. Please try again.')
    return render(request, 'registration/otp_verify.html')
