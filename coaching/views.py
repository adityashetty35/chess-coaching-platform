import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from django.http import JsonResponse
from core.decorators import coach_required

from .models import Batch, ChessClass, Attendance
from .forms import BatchForm, ChessClassForm

@coach_required
def batch_list(request):
    batches = Batch.objects.annotate(active_students=Count('students', filter=Q(students__status='active')))
    return render(request, 'coaching/batch_list.html', {'batches': batches, 'title': 'Batches'})

@coach_required
def batch_form(request, pk=None):
    if pk:
        batch = get_object_or_404(Batch, pk=pk)
        title = 'Edit Batch'
    else:
        batch = None
        title = 'Add Batch'

    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Batch saved successfully.')
            return redirect('coaching:batch_list')
    else:
        form = BatchForm(instance=batch)
    return render(request, 'coaching/batch_form.html', {'form': form, 'title': title, 'back_url': 'coaching:batch_list'})

@coach_required
def batch_delete(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        batch.delete()
        messages.success(request, 'Batch deleted successfully.')
    return redirect('coaching:batch_list')

@coach_required
def class_list(request):
    classes = ChessClass.objects.all().select_related('batch')
    
    # Filter
    date_filter = request.GET.get('date', 'all')
    status_filter = request.GET.get('status', '')
    
    today = timezone.localdate()
    if date_filter == 'today':
        classes = classes.filter(date=today)
    elif date_filter == 'week':
        start_week = today - datetime.timedelta(days=today.weekday())
        end_week = start_week + datetime.timedelta(days=6)
        classes = classes.filter(date__range=[start_week, end_week])
    elif date_filter == 'upcoming':
        classes = classes.filter(date__gte=today)
    elif date_filter == 'past':
        classes = classes.filter(date__lt=today)
        
    if status_filter:
        classes = classes.filter(status=status_filter)
        
    context = {
        'classes': classes,
        'title': 'Classes',
        'date_filter': date_filter,
        'status_filter': status_filter,
    }
    return render(request, 'coaching/class_list.html', context)

@coach_required
def class_form(request, pk=None):
    if pk:
        chess_class = get_object_or_404(ChessClass, pk=pk)
        title = 'Edit Class'
    else:
        chess_class = None
        title = 'Add Class'

    if request.method == 'POST':
        form = ChessClassForm(request.POST, instance=chess_class)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class saved successfully.')
            return redirect('coaching:class_list')
    else:
        form = ChessClassForm(instance=chess_class)
    return render(request, 'coaching/class_form.html', {'form': form, 'title': title, 'back_url': 'coaching:class_list'})

@coach_required
def class_detail(request, pk):
    chess_class = get_object_or_404(ChessClass, pk=pk)
    
    if chess_class.batch:
        students = chess_class.batch.students.filter(status='active')
    else:
        students = chess_class.students.all()
        
    attendances = {a.student_id: a for a in chess_class.attendance_records.all()}
    
    student_records = []
    for st in students:
        att = attendances.get(st.id)
        student_records.append({
            'student': st,
            'attendance': att
        })
        
    context = {
        'chess_class': chess_class,
        'student_records': student_records,
        'title': f'Class: {chess_class}'
    }
    return render(request, 'coaching/class_detail.html', context)

@coach_required
def class_delete(request, pk):
    chess_class = get_object_or_404(ChessClass, pk=pk)
    if request.method == 'POST':
        chess_class.delete()
        messages.success(request, 'Class deleted successfully.')
    return redirect('coaching:class_list')

@coach_required
def mark_attendance(request, pk):
    chess_class = get_object_or_404(ChessClass, pk=pk)
    
    if chess_class.batch:
        students = chess_class.batch.students.filter(status='active')
    else:
        students = chess_class.students.all()
        
    if request.method == 'POST':
        for st in students:
            status = request.POST.get(f'status_{st.id}')
            if status:
                Attendance.objects.update_or_create(
                    chess_class=chess_class,
                    student=st,
                    defaults={'status': status}
                )
        chess_class.status = 'completed'
        chess_class.save()
        messages.success(request, 'Attendance marked successfully.')
        return redirect('coaching:class_detail', pk=pk)
        
    attendances = {a.student_id: a.status for a in chess_class.attendance_records.all()}
    
    student_records = []
    for st in students:
        student_records.append({
            'student': st,
            'status': attendances.get(st.id, 'present')
        })
        
    context = {
        'chess_class': chess_class,
        'student_records': student_records,
        'title': 'Mark Attendance'
    }
    return render(request, 'coaching/mark_attendance.html', context)

@coach_required
def calendar_view(request):
    return render(request, 'coaching/calendar.html', {'title': 'Calendar'})

@coach_required
def calendar_events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    classes = ChessClass.objects.all()
    if start:
        classes = classes.filter(date__gte=start)
    if end:
        classes = classes.filter(date__lte=end)
        
    events = []
    for c in classes:
        start_dt = f"{c.date}T{c.start_time.strftime('%H:%M:%S')}"
        end_dt = f"{c.date}T{c.end_time.strftime('%H:%M:%S')}"
        title = c.title or c.topic or f"{c.get_class_type_display()} Class"
        
        if c.status == 'cancelled':
            color = '#dc3545'
        elif c.status == 'completed':
            color = '#198754'
        else:
            color = '#0d6efd'
            
        events.append({
            'id': c.id,
            'title': title,
            'start': start_dt,
            'end': end_dt,
            'url': f"/coaching/{c.id}/",
            'color': color
        })
        
    return JsonResponse(events, safe=False)
