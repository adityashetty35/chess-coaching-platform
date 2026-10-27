from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.decorators import coach_required
from core.permissions import role_for
from core.models import UserRole
from django.core.exceptions import PermissionDenied
from .models import Assignment, AssignmentSubmission
from .forms import AssignmentForm, SubmissionStatusForm


def visible_assignments(user):
    entries = Assignment.objects.all()
    return entries.filter(assigned_coach=user) if role_for(user) == UserRole.COACH else entries

@coach_required
def assignment_list(request):
    assignments = visible_assignments(request.user)
    return render(request, 'assignments/list.html', {
        'assignments': assignments,
        'title': 'Assignments'
    })

@coach_required
def assignment_form(request, pk=None):
    if not pk and role_for(request.user) == UserRole.COACH:
        raise PermissionDenied('Only administrators can assign new homework.')
    assignment = get_object_or_404(visible_assignments(request.user), pk=pk) if pk else None
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if role_for(request.user) == UserRole.COACH:
            form.fields.pop('assigned_coach')
            form.fields['batch'].queryset = form.fields['batch'].queryset.filter(pk=assignment.batch_id)
            form.fields['students'].queryset = assignment.students.all()
        if form.is_valid():
            assignment = form.save()
            students = set(assignment.students.all())
            if assignment.batch:
                students |= set(assignment.batch.students.filter(status='active'))
            for student in students:
                AssignmentSubmission.objects.get_or_create(
                    assignment=assignment, student=student
                )
            messages.success(request, 'Assignment saved successfully.')
            return redirect('assignments:list')
    else:
        form = AssignmentForm(instance=assignment)
        if role_for(request.user) == UserRole.COACH:
            form.fields.pop('assigned_coach')
        
    return render(request, 'assignments/form.html', {
        'form': form,
        'title': 'Edit Assignment' if pk else 'Add Assignment'
    })

@coach_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(visible_assignments(request.user), pk=pk)
    submissions = assignment.submissions.all().select_related('student__user')
    status_form = SubmissionStatusForm()
    return render(request, 'assignments/detail.html', {
        'assignment': assignment,
        'submissions': submissions,
        'status_form': status_form,
        'title': assignment.title
    })

@require_POST
@coach_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(visible_assignments(request.user), pk=pk)
    assignment.delete()
    messages.success(request, 'Assignment deleted.')
    return redirect('assignments:list')

@require_POST
@coach_required
def update_submission_status(request, pk, submission_pk):
    get_object_or_404(visible_assignments(request.user), pk=pk)
    submission = get_object_or_404(AssignmentSubmission, pk=submission_pk, assignment_id=pk)
    form = SubmissionStatusForm(request.POST, instance=submission)
    if form.is_valid():
        form.save()
        messages.success(request, 'Submission updated.')
    else:
        messages.error(request, 'Failed to update submission.')
    return redirect('assignments:detail', pk=pk)
