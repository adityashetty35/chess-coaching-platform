from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.decorators import coach_required
from .models import *
from .forms import *

@coach_required
def dashboard(request):
    from students.models import Student
    from students.models import Parent
    from enquiries.models import Enquiry
    from coaching.models import ChessClass, Attendance
    from fees.models import Invoice
    from progress.models import TestResult, ScheduledTest
    from django.utils import timezone
    from django.db.models import Sum, F, DecimalField

    today = timezone.now().date()
    unpaid = Invoice.objects.exclude(status='cancelled').filter(amount__gt=F('amount_paid'))
    attendance_today = Attendance.objects.filter(chess_class__date=today)
    context = {
        'active_students': Student.objects.filter(status='active').count(),
        'new_enquiries': Enquiry.objects.filter(status='new').count(),
        'pending_fees_total': unpaid.aggregate(total=Sum(
            F('amount') - F('amount_paid'), output_field=DecimalField(max_digits=12, decimal_places=2)
        ))['total'] or 0,
        'tests_recorded': TestResult.objects.count(),
        'upcoming_test': ScheduledTest.objects.filter(date__gte=today).first(),
        'next_lesson': ChessClass.objects.filter(date__gte=today, status='scheduled').order_by('date', 'start_time').first(),
        'attendance_marked_today': attendance_today.count(),
        'attendance_present_today': attendance_today.filter(status__in=['present', 'late']).count(),
        'parent_count': Parent.objects.count(),
        'recent_enquiries': Enquiry.objects.order_by('-created_at')[:4],
        'upcoming_test_count': ScheduledTest.objects.filter(date__gte=today).count(),
    }
    return render(request, 'core/dashboard_academy.html', context)


@coach_required
def settings_view(request):
    from .forms import AcademySettingsForm
    settings = SiteSettings.load()
    form = AcademySettingsForm(request.POST or None, request.FILES or None, instance=settings)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Settings updated successfully.")
        return redirect("settings:index")
    return render(request, "core/settings_academy.html", {"form": form})


@coach_required
def services_list(request):
    services = CoachingService.objects.all()
    return render(request, "core/services_list.html", {"services": services})

@coach_required
def service_form(request, pk=None):
    instance = get_object_or_404(CoachingService, pk=pk) if pk else None
    form = CoachingServiceForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Service saved.")
        return redirect("settings:services")
    return render(request, "core/generic_form.html", {"form": form, "title": "Service", "back_url": "settings:services"})

@coach_required
def service_delete(request, pk):
    get_object_or_404(CoachingService, pk=pk).delete()
    messages.success(request, "Service deleted.")
    return redirect("settings:services")

@coach_required
def programs_list(request):
    programs = CoachingProgram.objects.all()
    return render(request, "core/programs_list.html", {"programs": programs})

@coach_required
def program_form(request, pk=None):
    instance = get_object_or_404(CoachingProgram, pk=pk) if pk else None
    form = CoachingProgramForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Program saved.")
        return redirect("settings:programs")
    return render(request, "core/generic_form.html", {"form": form, "title": "Program", "back_url": "settings:programs"})

@coach_required
def program_delete(request, pk):
    get_object_or_404(CoachingProgram, pk=pk).delete()
    messages.success(request, "Program deleted.")
    return redirect("settings:programs")

@coach_required
def testimonials_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, "core/testimonials_list.html", {"testimonials": testimonials})

@coach_required
def testimonial_form(request, pk=None):
    instance = get_object_or_404(Testimonial, pk=pk) if pk else None
    form = TestimonialForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Testimonial saved.")
        return redirect("settings:testimonials")
    return render(request, "core/generic_form.html", {"form": form, "title": "Testimonial", "back_url": "settings:testimonials"})

@coach_required
def testimonial_delete(request, pk):
    get_object_or_404(Testimonial, pk=pk).delete()
    messages.success(request, "Testimonial deleted.")
    return redirect("settings:testimonials")

@coach_required
def faqs_list(request):
    faqs = FAQ.objects.all()
    return render(request, "core/faqs_list.html", {"faqs": faqs})

@coach_required
def faq_form(request, pk=None):
    instance = get_object_or_404(FAQ, pk=pk) if pk else None
    form = FAQForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "FAQ saved.")
        return redirect("settings:faqs")
    return render(request, "core/generic_form.html", {"form": form, "title": "FAQ", "back_url": "settings:faqs"})

@coach_required
def faq_delete(request, pk):
    get_object_or_404(FAQ, pk=pk).delete()
    messages.success(request, "FAQ deleted.")
    return redirect("settings:faqs")

@coach_required
def achievements_list(request):
    achievements = Achievement.objects.all()
    return render(request, "core/achievements_list.html", {"achievements": achievements})

@coach_required
def achievement_form(request, pk=None):
    instance = get_object_or_404(Achievement, pk=pk) if pk else None
    form = AchievementForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Achievement saved.")
        return redirect("settings:achievements")
    return render(request, "core/generic_form.html", {"form": form, "title": "Achievement", "back_url": "settings:achievements"})

@coach_required
def achievement_delete(request, pk):
    get_object_or_404(Achievement, pk=pk).delete()
    messages.success(request, "Achievement deleted.")
    return redirect("settings:achievements")
