from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.decorators import coach_required
from .models import Assignment, AssignmentSubmission
from .forms import AssignmentForm, SubmissionStatusForm

@coach_required
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/list.html', {
        'assignments': assignments,
        'title': 'Assignments'
    })

@coach_required
def assignment_form(request, pk=None):
    assignment = get_object_or_404(Assignment, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
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
        
    return render(request, 'assignments/form.html', {
        'form': form,
        'title': 'Edit Assignment' if pk else 'Add Assignment'
    })

@coach_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
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
    assignment = get_object_or_404(Assignment, pk=pk)
    assignment.delete()
    messages.success(request, 'Assignment deleted.')
    return redirect('assignments:list')

@require_POST
@coach_required
def update_submission_status(request, pk, submission_pk):
    submission = get_object_or_404(AssignmentSubmission, pk=submission_pk, assignment_id=pk)
    form = SubmissionStatusForm(request.POST, instance=submission)
    if form.is_valid():
        form.save()
        messages.success(request, 'Submission updated.')
    else:
        messages.error(request, 'Failed to update submission.')
    return redirect('assignments:detail', pk=pk)
