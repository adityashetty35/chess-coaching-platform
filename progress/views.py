from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django import forms
from core.decorators import coach_required
from .models import ProgressEntry, Goal, SyllabusLesson, TestResult, FideRatingRecord, ScheduledTest
from .forms import ProgressEntryForm, GoalForm, SyllabusLessonForm, TestResultForm, FideRatingRecordForm, ScheduledTestForm
from students.models import Student

@coach_required
def progress_list(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    entries = ProgressEntry.objects.filter(student=student)
    return render(request, 'progress/list.html', {
        'student': student,
        'entries': entries,
        'title': f"Progress: {student.user.get_full_name()}"
    })

@coach_required
def progress_form(request, student_pk, pk=None):
    student = get_object_or_404(Student, pk=student_pk)
    entry = get_object_or_404(ProgressEntry, pk=pk, student=student) if pk else None
    
    if request.method == 'POST':
        form = ProgressEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.student = student
            entry.save()
            messages.success(request, 'Progress entry saved.')
            return redirect('progress:list', student_pk=student.pk)
    else:
        form = ProgressEntryForm(instance=entry)
        
    return render(request, 'progress/form.html', {
        'form': form,
        'student': student,
        'title': 'Edit Progress Entry' if pk else 'Add Progress Entry'
    })

@require_POST
@coach_required
def progress_delete(request, student_pk, pk):
    entry = get_object_or_404(ProgressEntry, pk=pk, student_id=student_pk)
    entry.delete()
    messages.success(request, 'Progress entry deleted.')
    return redirect('progress:list', student_pk=student_pk)

@coach_required
def goal_list(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    goals = Goal.objects.filter(student=student)
    return render(request, 'progress/goal_list.html', {
        'student': student,
        'goals': goals,
        'title': f"Goals: {student.user.get_full_name()}"
    })

@coach_required
def goal_form(request, student_pk, pk=None):
    student = get_object_or_404(Student, pk=student_pk)
    goal = get_object_or_404(Goal, pk=pk, student=student) if pk else None
    
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            g = form.save(commit=False)
            g.student = student
            g.save()
            messages.success(request, 'Goal saved.')
            return redirect('progress:goal_list', student_pk=student.pk)
    else:
        form = GoalForm(instance=goal)
        
    return render(request, 'progress/goal_form.html', {
        'form': form,
        'student': student,
        'title': 'Edit Goal' if pk else 'Add Goal'
    })

@require_POST
@coach_required
def goal_delete(request, student_pk, pk):
    goal = get_object_or_404(Goal, pk=pk, student_id=student_pk)
    goal.delete()
    messages.success(request, 'Goal deleted.')
    return redirect('progress:goal_list', student_pk=student_pk)


@coach_required
def academy_records(request):
    return render(request, 'progress/academy_records.html', {
        'lessons': SyllabusLesson.objects.all(),
        'tests': TestResult.objects.select_related('student')[:40],
        'ratings': FideRatingRecord.objects.select_related('student', 'verified_by')[:40],
        'scheduled_tests': ScheduledTest.objects.select_related('batch').all()[:40],
    })


@coach_required
def academy_record_form(request, kind, pk=None):
    config = {
        'lesson': (SyllabusLesson, SyllabusLessonForm),
        'test': (TestResult, TestResultForm),
        'fide': (FideRatingRecord, FideRatingRecordForm),
        'schedule': (ScheduledTest, ScheduledTestForm),
    }
    if kind not in config:
        from django.http import Http404
        raise Http404()
    model, form_class = config[kind]
    instance = get_object_or_404(model, pk=pk) if pk else None
    form = form_class(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        record = form.save(commit=False)
        if kind == 'fide' and not pk:
            record.verified_by = request.user
        record.save()
        messages.success(request, 'Record saved.')
        return redirect('progress:academy_records')
    for field in form.fields.values():
        if not isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.setdefault('class', 'form-select' if isinstance(field.widget, forms.Select) else 'form-control')
    return render(request, 'progress/academy_record_form.html', {
        'form': form, 'title': {'lesson': 'Syllabus lesson', 'test': 'Test result', 'fide': 'Verified FIDE rating', 'schedule': 'Upcoming test'}[kind],
    })
