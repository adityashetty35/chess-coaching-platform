import csv
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from core.decorators import coach_required
from students.models import Student
from enquiries.models import Enquiry
from coaching.models import Attendance
from fees.models import Invoice, Payment

@coach_required
def reports_index(request):
    today = date.today()
    month_start = today.replace(day=1)
    context = {
        'total_students': Student.objects.filter(status='active').count(),
        'total_enquiries': Enquiry.objects.count(),
        'enquiry_conversion': Enquiry.objects.filter(status='converted').count(),
        'fees_collected': Payment.objects.filter(payment_date__gte=month_start).aggregate(t=Sum('amount'))['t'] or 0,
        'pending_fees': Invoice.objects.filter(status__in=['pending', 'partially_paid', 'overdue']).aggregate(t=Sum('amount') - Sum('amount_paid'))['t'] or 0,
    }
    return render(request, 'reports/index.html', context)

@coach_required
def fees_report(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    status = request.GET.get('status', '')

    invoices = Invoice.objects.select_related('student').all()
    if start:
        invoices = invoices.filter(due_date__gte=start)
    if end:
        invoices = invoices.filter(due_date__lte=end)
    if status:
        invoices = invoices.filter(status=status)

    total_amount = invoices.aggregate(t=Sum('amount'))['t'] or 0
    total_paid = invoices.aggregate(t=Sum('amount_paid'))['t'] or 0
    total_pending = total_amount - total_paid

    payments = Payment.objects.select_related('invoice__student').all()
    if start:
        payments = payments.filter(payment_date__gte=start)
    if end:
        payments = payments.filter(payment_date__lte=end)

    context = {
        'invoices': invoices,
        'payments': payments,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'filter_start': start or '',
        'filter_end': end or '',
        'filter_status': status,
    }
    return render(request, 'reports/fees.html', context)

@coach_required
def students_report(request):
    status = request.GET.get('status', 'active')
    level = request.GET.get('level', '')
    batch = request.GET.get('batch', '')

    students = Student.objects.all()
    if status:
        students = students.filter(status=status)
    if level:
        students = students.filter(chess_level=level)
    if batch:
        students = students.filter(batch_id=batch)

    context = {
        'students': students,
        'filter_status': status,
        'filter_level': level,
        'filter_batch': batch,
    }
    return render(request, 'reports/students.html', context)

@coach_required
def attendance_report(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    student_id = request.GET.get('student', '')

    records = Attendance.objects.select_related('student', 'chess_class').all()
    if start:
        records = records.filter(chess_class__date__gte=start)
    if end:
        records = records.filter(chess_class__date__lte=end)
    if student_id:
        records = records.filter(student_id=student_id)

    total = records.count()
    present = records.filter(status__in=['present', 'late']).count()
    absent = records.filter(status='absent').count()

    student_summary = []
    for s in Student.objects.filter(status='active'):
        s_records = records.filter(student=s)
        s_total = s_records.count()
        s_present = s_records.filter(status__in=['present', 'late']).count()
        pct = round(s_present / s_total * 100) if s_total > 0 else 0
        student_summary.append({
            'student': s,
            'total': s_total,
            'present': s_present,
            'absent': s_records.filter(status='absent').count(),
            'percentage': pct,
        })
    student_summary.sort(key=lambda x: x['percentage'])

    context = {
        'records': records[:100],
        'total': total,
        'present': present,
        'absent': absent,
        'overall_pct': round(present / total * 100) if total > 0 else 0,
        'student_summary': student_summary,
        'filter_start': start or '',
        'filter_end': end or '',
        'filter_student': student_id,
        'students': Student.objects.filter(status='active'),
    }
    return render(request, 'reports/attendance.html', context)

@coach_required
def enquiries_report(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    enquiries = Enquiry.objects.all()
    if start:
        enquiries = enquiries.filter(created_at__date__gte=start)
    if end:
        enquiries = enquiries.filter(created_at__date__lte=end)

    status_counts = {}
    for code, label in Enquiry.STATUS_CHOICES:
        status_counts[label] = enquiries.filter(status=code).count()

    total = enquiries.count()
    converted = enquiries.filter(status='converted').count()
    conversion_rate = round(converted / total * 100) if total > 0 else 0

    context = {
        'enquiries': enquiries,
        'status_counts': status_counts,
        'total': total,
        'converted': converted,
        'conversion_rate': conversion_rate,
        'filter_start': start or '',
        'filter_end': end or '',
    }
    return render(request, 'reports/enquiries.html', context)

@coach_required
def export_csv(request, report_type):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'
    writer = csv.writer(response)

    if report_type == 'students':
        writer.writerow(['Name', 'Status', 'Level', 'Coaching Type', 'Batch', 'Joining Date', 'Phone', 'Email', 'FIDE Rating'])
        for s in Student.objects.all():
            writer.writerow([s.full_name, s.get_status_display(), s.get_chess_level_display(), s.get_coaching_type_display(), str(s.batch) if s.batch else '', s.joining_date, s.phone, s.email, s.fide_rating or ''])
    elif report_type == 'fees':
        writer.writerow(['Student', 'Description', 'Amount', 'Paid', 'Balance', 'Due Date', 'Status'])
        for inv in Invoice.objects.select_related('student').all():
            writer.writerow([inv.student.full_name, inv.description, inv.amount, inv.amount_paid, inv.balance, inv.due_date, inv.get_status_display()])
    elif report_type == 'payments':
        writer.writerow(['Date', 'Student', 'Amount', 'Method', 'Reference', 'Invoice'])
        for p in Payment.objects.select_related('invoice__student').all():
            writer.writerow([p.payment_date, p.invoice.student.full_name, p.amount, p.get_method_display(), p.reference, p.invoice.description])
    elif report_type == 'attendance':
        writer.writerow(['Student', 'Total Classes', 'Present', 'Absent', 'Late', 'Excused', 'Attendance %'])
        for s in Student.objects.filter(status='active'):
            records = s.attendance_records.all()
            total = records.count()
            present = records.filter(status='present').count()
            late = records.filter(status='late').count()
            absent = records.filter(status='absent').count()
            excused = records.filter(status='excused').count()
            pct = round((present + late) / total * 100) if total > 0 else 0
            writer.writerow([s.full_name, total, present, absent, late, excused, pct])
    elif report_type == 'enquiries':
        writer.writerow(['Name', 'Parent', 'Phone', 'Email', 'Level', 'Status', 'Source', 'Date'])
        for e in Enquiry.objects.all():
            writer.writerow([e.student_name, e.parent_name, e.phone, e.email, e.get_current_level_display(), e.get_status_display(), e.source, e.created_at.strftime('%Y-%m-%d')])
    return response
