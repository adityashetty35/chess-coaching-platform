from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.decorators import coach_required
from .models import *
from .forms import *

@coach_required
def dashboard(request):
    from students.models import Student
    from enquiries.models import Enquiry
    from coaching.models import ChessClass, Attendance
    from fees.models import Invoice, Payment, PaymentReminder
    from django.utils import timezone
    from django.db.models import Sum, Q
    from datetime import timedelta

    today = timezone.now().date()

    context = {
        "active_students": Student.objects.filter(status="active").count(),
        "new_enquiries": Enquiry.objects.filter(status="new").count(),
        "today_classes": ChessClass.objects.filter(date=today, status="scheduled"),
        "upcoming_classes": ChessClass.objects.filter(date__gt=today, status="scheduled").order_by("date", "start_time")[:5],
        "pending_invoices": Invoice.objects.filter(status__in=["pending", "partially_paid"]),
        "overdue_invoices": Invoice.objects.filter(status="overdue"),
        "recent_payments": Payment.objects.order_by("-payment_date", "-created_at")[:5],
        "upcoming_reminders": PaymentReminder.objects.filter(status="pending", scheduled_date__gte=today).order_by("scheduled_date")[:5],
        "follow_up_enquiries": Enquiry.objects.filter(status="follow_up", follow_up_date__lte=today),
        "fees_collected_month": Payment.objects.filter(
            payment_date__year=today.year, payment_date__month=today.month
        ).aggregate(total=Sum("amount"))["total"] or 0,
        "pending_fees_total": Invoice.objects.filter(
            status__in=["pending", "partially_paid", "overdue"]
        ).aggregate(total=Sum("amount") - Sum("amount_paid"))["total"] or 0,
        "low_attendance_students": [],
    }

    # Low attendance - students with < 70% in last 30 days
    active_students = Student.objects.filter(status="active")
    low_att = []
    for s in active_students:
        records = Attendance.objects.filter(student=s, chess_class__date__gte=today - timedelta(days=30))
        total = records.count()
        if total >= 3:
            present = records.filter(status__in=["present", "late"]).count()
            pct = round(present / total * 100)
            if pct < 70:
                low_att.append({"student": s, "percentage": pct})
    context["low_attendance_students"] = low_att

    return render(request, "core/dashboard.html", context)


@coach_required
def settings_view(request):
    settings = SiteSettings.load()
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=settings)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Settings updated successfully.")
        return redirect("settings:index")
    return render(request, "core/settings.html", {"form": form})


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
