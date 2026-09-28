from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse

from core.decorators import coach_required
from .models import Student, Parent
from .forms import StudentForm, ParentForm

try:
    from coaching.models import ChessClass, Attendance
except ImportError:
    # Fallback
    pass

try:
    from fees.models import Invoice
except ImportError:
    pass

try:
    from progress.models import ProgressEntry, Goal
except ImportError:
    pass

try:
    from tournaments.models import TournamentResult
except ImportError:
    pass

try:
    from assignments.models import AssignmentSubmission
except ImportError:
    pass

@coach_required
def student_list(request):
    students = Student.objects.all()
    
    status = request.GET.get('status')
    level = request.GET.get('level')
    batch = request.GET.get('batch')
    coaching_type = request.GET.get('coaching_type')
    search = request.GET.get('q')

    if status:
        students = students.filter(status=status)
    if level:
        students = students.filter(chess_level=level)
    if batch:
        students = students.filter(batch_id=batch)
    if coaching_type:
        students = students.filter(coaching_type=coaching_type)
    if search:
        students = students.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
        
    context = {
        'students': students,
        'title': 'Students'
    }
    return render(request, 'students/list.html', context)

@coach_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    attendance_pct = 0
    try:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status__in=['present', 'late']).count()
        attendance_pct = round(present / total * 100) if total > 0 else 0
    except Exception:
        pass
        
    recent_classes = []
    try:
        recent_classes = Attendance.objects.filter(student=student).select_related('chess_class').order_by('-chess_class__date')[:5]
    except Exception:
        pass
        
    invoices = []
    try:
        invoices = Invoice.objects.filter(student=student).order_by('-due_date')
    except Exception:
        pass

    progress_entries = []
    goals = []
    try:
        progress_entries = ProgressEntry.objects.filter(student=student).order_by('-date')
        goals = Goal.objects.filter(student=student).order_by('-created_at')
    except Exception:
        pass

    tournaments = []
    try:
        tournaments = TournamentResult.objects.filter(student=student).order_by('-tournament__start_date')
    except Exception:
        pass

    assignments = []
    try:
        assignments = AssignmentSubmission.objects.filter(student=student).order_by('-submitted_at')
    except Exception:
        pass
    
    context = {
        'student': student,
        'title': f"{student.full_name}'s Profile",
        'attendance_pct': attendance_pct,
        'recent_classes': recent_classes,
        'invoices': invoices,
        'progress_entries': progress_entries,
        'goals': goals,
        'tournaments': tournaments,
        'assignments': assignments,
    }
    return render(request, 'students/detail.html', context)

@coach_required
def student_form(request, student_id=None):
    if student_id:
        student = get_object_or_404(Student, id=student_id)
        title = "Edit Student"
        back_url_str = reverse('students:detail', args=[student.id])
    else:
        student = None
        title = "Add Student"
        back_url_str = reverse('students:list')
        
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            saved_student = form.save()
            messages.success(request, f"Student '{saved_student.full_name}' saved successfully.")
            return redirect('students:detail', student_id=saved_student.id)
    else:
        form = StudentForm(instance=student)
        
    context = {
        'form': form,
        'title': title,
        'student': student,
        'back_url_str': back_url_str
    }
    return render(request, 'students/form.html', context)

@coach_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f"Student '{name}' deleted successfully.")
        return redirect('students:list')
    return redirect('students:detail', student_id=student.id)

@coach_required
def create_student_login(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        if not student.user:
            username = f"{student.first_name.lower()}.{student.last_name.lower()}".replace(' ','')
            # Handle duplicate username if necessary
            if User.objects.filter(username=username).exists():
                username = f"{username}{student.id}"
                
            user = User.objects.create_user(
                username=username, 
                password='chess123', 
                first_name=student.first_name, 
                last_name=student.last_name, 
                email=student.email
            )
            student.user = user
            student.save()
            messages.success(request, f"Login created successfully for {student.full_name}. Username: {username}")
        else:
            messages.warning(request, f"Login already exists for {student.full_name}.")
            
    return redirect('students:detail', student_id=student.id)

@coach_required
def parent_list(request):
    parents = Parent.objects.all().prefetch_related('students')
    context = {
        'parents': parents,
        'title': 'Parents'
    }
    return render(request, 'students/parent_list.html', context)

@coach_required
def parent_form(request, parent_id=None):
    if parent_id:
        parent = get_object_or_404(Parent, id=parent_id)
        title = "Edit Parent"
    else:
        parent = None
        title = "Add Parent"
        
    if request.method == 'POST':
        form = ParentForm(request.POST, instance=parent)
        if form.is_valid():
            saved_parent = form.save()
            messages.success(request, f"Parent '{saved_parent.name}' saved successfully.")
            return redirect('students:parent_list')
    else:
        form = ParentForm(instance=parent)
        
    context = {
        'form': form,
        'title': title,
        'parent': parent,
        'back_url_str': reverse('students:parent_list')
    }
    return render(request, 'students/parent_form.html', context)

@coach_required
def parent_delete(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == 'POST':
        name = parent.name
        parent.delete()
        messages.success(request, f"Parent '{name}' deleted successfully.")
    return redirect('students:parent_list')

@coach_required
def create_parent_login(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == 'POST':
        if not parent.user:
            # Generate username from name
            parts = parent.name.lower().split()
            username = ".".join(parts) if len(parts) > 1 else parts[0]
            if User.objects.filter(username=username).exists():
                username = f"{username}{parent.id}"
                
            user = User.objects.create_user(
                username=username, 
                password='chess123', 
                first_name=parts[0],
                last_name=" ".join(parts[1:]) if len(parts) > 1 else "",
                email=parent.email
            )
            parent.user = user
            parent.save()
            messages.success(request, f"Login created successfully for {parent.name}. Username: {username}")
        else:
            messages.warning(request, f"Login already exists for {parent.name}.")
            
    return redirect('students:parent_list')
