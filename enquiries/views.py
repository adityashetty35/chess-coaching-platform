from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from core.decorators import coach_required
from .models import Enquiry, EnquiryFollowUp
from .forms import EnquiryForm, FollowUpForm
from students.models import Student, Parent


@coach_required
def enquiry_list(request):
    enquiries = Enquiry.objects.all()
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')

    if status_filter:
        enquiries = enquiries.filter(status=status_filter)
    if search_query:
        enquiries = enquiries.filter(
            student_name__icontains=search_query
        ) | enquiries.filter(
            phone__icontains=search_query
        ) | enquiries.filter(
            email__icontains=search_query
        )

    return render(request, 'enquiries/list.html', {
        'enquiries': enquiries,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Enquiry.STATUS_CHOICES,
    })


@coach_required
def enquiry_detail(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    follow_up_form = FollowUpForm()
    follow_ups = enquiry.follow_ups.all()

    return render(request, 'enquiries/detail.html', {
        'enquiry': enquiry,
        'follow_up_form': follow_up_form,
        'follow_ups': follow_ups,
        'status_choices': Enquiry.STATUS_CHOICES,
    })


@coach_required
def enquiry_form(request, pk=None):
    enquiry = get_object_or_404(Enquiry, pk=pk) if pk else None
    if request.method == 'POST':
        form = EnquiryForm(request.POST, instance=enquiry)
        if form.is_valid():
            enquiry = form.save()
            messages.success(request, 'Enquiry saved successfully.')
            return redirect('enquiries:detail', pk=enquiry.pk)
    else:
        form = EnquiryForm(instance=enquiry)

    return render(request, 'enquiries/form.html', {
        'form': form,
        'enquiry': enquiry,
    })


@coach_required
def update_status(request, pk):
    if request.method == 'POST':
        enquiry = get_object_or_404(Enquiry, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Enquiry.STATUS_CHOICES):
            enquiry.status = new_status
            enquiry.save()
            messages.success(request, f'Status updated to {enquiry.get_status_display()}.')
    return redirect('enquiries:detail', pk=pk)


@coach_required
def add_follow_up(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        form = FollowUpForm(request.POST)
        if form.is_valid():
            follow_up = form.save(commit=False)
            follow_up.enquiry = enquiry
            follow_up.save()

            if follow_up.next_follow_up:
                enquiry.follow_up_date = follow_up.next_follow_up
                enquiry.save()

            messages.success(request, 'Follow-up note added successfully.')
    return redirect('enquiries:detail', pk=pk)


@coach_required
def convert_to_student(request, pk):
    if request.method == 'POST':
        enquiry = get_object_or_404(Enquiry, pk=pk)

        if enquiry.status == 'converted' and enquiry.converted_student:
            messages.warning(request, 'This enquiry is already converted.')
            return redirect('students:detail', pk=enquiry.converted_student.pk)

        parts = enquiry.student_name.strip().split(' ', 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=enquiry.email,
            phone=enquiry.phone,
            whatsapp=enquiry.whatsapp or enquiry.phone,
            joining_date=timezone.now().date(),
            chess_level=enquiry.current_level,
            preferred_mode=enquiry.preferred_mode,
            chess_goals=enquiry.coaching_goal,
            notes=f'Converted from website enquiry on {timezone.now().date()}.\nOriginal Message: {enquiry.message}'
        )

        if enquiry.parent_name:
            parent = Parent.objects.create(
                name=enquiry.parent_name,
                relationship='guardian',
                phone=enquiry.phone,
                whatsapp=enquiry.whatsapp or enquiry.phone,
                email=enquiry.email,
            )
            parent.students.add(student)

        enquiry.status = 'converted'
        enquiry.converted_student = student
        enquiry.save()

        messages.success(request, f'Successfully converted {enquiry.student_name} to student profile.')
        return redirect('students:detail', pk=student.pk)

    return redirect('enquiries:detail', pk=pk)


@coach_required
def enquiry_delete(request, pk):
    if request.method == 'POST':
        enquiry = get_object_or_404(Enquiry, pk=pk)
        enquiry.delete()
        messages.success(request, 'Enquiry deleted successfully.')
    return redirect('enquiries:list')
