from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from students.models import Student
from coaching.models import ChessClass, Attendance
from fees.models import Invoice
from progress.models import ProgressEntry, Goal
from tournaments.models import TournamentResult
from assignments.models import AssignmentSubmission
from announcements.models import Announcement

def get_portal_students(user):
    students = []
    if hasattr(user, 'student_profile'):
        students = [user.student_profile]
    elif hasattr(user, 'parent_profile'):
        students = list(user.parent_profile.students.all())
    return students

@login_required
def portal_dashboard(request):
    if request.user.is_staff:
        return redirect('core:dashboard')

    students = get_portal_students(request.user)
    if not students:
        return render(request, 'portal/no_access.html')

    today = timezone.now().date()
    is_parent = hasattr(request.user, 'parent_profile')

    context = {
        'students': students,
        'is_parent': is_parent,
        'upcoming_classes': ChessClass.objects.filter(
            students__in=students, date__gte=today, status='scheduled'
        ).distinct().order_by('date', 'start_time')[:5],
        'recent_announcements': Announcement.objects.filter(
            is_active=True
        ).order_by('-publish_date')[:5],
        'pending_homework': AssignmentSubmission.objects.filter(
            student__in=students, status__in=['pending', 'in_progress']
        ).select_related('assignment')[:5],
    }

    if is_parent:
        context['pending_fees'] = Invoice.objects.filter(
            student__in=students, status__in=['pending', 'partially_paid', 'overdue']
        )

    return render(request, 'portal/dashboard.html', context)

@login_required
def portal_classes(request):
    students = get_portal_students(request.user)
    today = timezone.now().date()
    from django.db.models import Q
    batches = [s.batch for s in students if s.batch]

    base_query = ChessClass.objects.filter(
        Q(students__in=students) | Q(batch__in=batches)
    ).distinct()

    upcoming = base_query.filter(date__gte=today, status='scheduled').order_by('date', 'start_time')
    past = base_query.filter(date__lt=today).order_by('-date', '-start_time')[:20]

    return render(request, 'portal/classes.html', {
        'upcoming': upcoming,
        'past': past,
        'students': students,
    })

@login_required
def portal_attendance(request):
    students = get_portal_students(request.user)
    attendance_data = []

    for student in students:
        records = Attendance.objects.filter(student=student).select_related('chess_class').order_by('-chess_class__date')
        total = records.count()
        present = records.filter(status__in=['present', 'late']).count()
        pct = round(present / total * 100) if total > 0 else 0
        attendance_data.append({
            'student': student,
            'records': records[:30],
            'total': total,
            'present': present,
            'percentage': pct,
        })

    return render(request, 'portal/attendance.html', {
        'attendance_data': attendance_data,
        'students': students,
    })

@login_required
def portal_homework(request):
    students = get_portal_students(request.user)
    submissions = AssignmentSubmission.objects.filter(
        student__in=students
    ).select_related('assignment', 'student').order_by('-assignment__due_date')

    return render(request, 'portal/homework.html', {
        'submissions': submissions,
        'students': students,
    })

@login_required
def portal_progress(request):
    students = get_portal_students(request.user)
    progress_data = []

    for student in students:
        entries = ProgressEntry.objects.filter(student=student).order_by('-date')
        progress_data.append({
            'student': student,
            'entries': entries[:10],
            'latest': entries.first(),
        })

    return render(request, 'portal/progress.html', {
        'progress_data': progress_data,
        'students': students,
    })

@login_required
def portal_goals(request):
    students = get_portal_students(request.user)
    goals = Goal.objects.filter(student__in=students).select_related('student')

    return render(request, 'portal/goals.html', {
        'goals': goals,
        'students': students,
    })

@login_required
def portal_tournaments(request):
    students = get_portal_students(request.user)
    results = TournamentResult.objects.filter(
        student__in=students
    ).select_related('student').order_by('-date')

    return render(request, 'portal/tournaments.html', {
        'results': results,
        'students': students,
    })

@login_required
def portal_fees(request):
    students = get_portal_students(request.user)
    invoices = Invoice.objects.filter(student__in=students).select_related('student')

    return render(request, 'portal/fees.html', {
        'invoices': invoices,
        'students': students,
    })

@login_required
def portal_announcements(request):
    students = get_portal_students(request.user)
    announcements = Announcement.objects.filter(is_active=True).order_by('-publish_date')

    filtered = []
    for ann in announcements:
        if ann.audience == 'everyone':
            filtered.append(ann)
        elif ann.audience == 'students' and hasattr(request.user, 'student_profile'):
            filtered.append(ann)
        elif ann.audience == 'parents' and hasattr(request.user, 'parent_profile'):
            filtered.append(ann)
        elif ann.audience == 'batch':
            for s in students:
                if s.batch and ann.batch_id == s.batch_id:
                    filtered.append(ann)
                    break
        elif ann.audience == 'individual':
            if any(s in ann.students.all() for s in students):
                filtered.append(ann)

    return render(request, 'portal/announcements.html', {
        'announcements': filtered,
        'students': students,
    })
