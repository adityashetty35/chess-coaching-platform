import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.decorators import coach_required
from core.models import SiteSettings
from .models import FeePlan, Invoice, Payment, PaymentReminder
from .forms import FeePlanForm, InvoiceForm, PaymentForm, ReminderForm
from students.models import Student
from django.utils import timezone

@coach_required
def fee_plan_list(request):
    plans = FeePlan.objects.all()
    return render(request, 'fees/plan_list.html', {'items': plans})

@coach_required
def fee_plan_form(request, pk=None):
    plan = get_object_or_404(FeePlan, pk=pk) if pk else None
    if request.method == 'POST':
        form = FeePlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee plan saved successfully.')
            return redirect('fees:plan_list')
    else:
        form = FeePlanForm(instance=plan)
    
    title = 'Edit Fee Plan' if plan else 'Add Fee Plan'
    return render(request, 'fees/plan_form.html', {
        'form': form,
        'title': title,
        'back_url': 'fees:plan_list'
    })

@coach_required
@require_POST
def fee_plan_delete(request, pk):
    plan = get_object_or_404(FeePlan, pk=pk)
    plan.delete()
    messages.success(request, 'Fee plan deleted.')
    return redirect('fees:plan_list')

@coach_required
def invoice_list(request):
    invoices = Invoice.objects.select_related('student', 'fee_plan').all()
    
    status_filter = request.GET.get('status')
    if status_filter:
        invoices = invoices.filter(status=status_filter)
        
    student_filter = request.GET.get('student')
    if student_filter:
        invoices = invoices.filter(student_id=student_filter)
        
    search_query = request.GET.get('search')
    if search_query:
        invoices = invoices.filter(description__icontains=search_query)

    students = Student.objects.filter(status='active').order_by('first_name')
    return render(request, 'fees/invoice_list.html', {
        'items': invoices,
        'students': students,
        'status_filter': status_filter,
        'student_filter': student_filter,
        'search_query': search_query,
    })

@coach_required
def invoice_form(request, pk=None):
    invoice = get_object_or_404(Invoice, pk=pk) if pk else None
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            inv = form.save()
            inv.update_status()
            messages.success(request, 'Invoice saved successfully.')
            return redirect('fees:invoice_detail', pk=inv.pk)
    else:
        form = InvoiceForm(instance=invoice)
    
    fee_plans = FeePlan.objects.filter(is_active=True)
    if invoice:
        title = 'Edit Invoice'
        back_url = reverse('fees:invoice_detail', kwargs={'pk': invoice.pk})
    else:
        title = 'Add Invoice'
        back_url = reverse('fees:invoice_list')
        
    return render(request, 'fees/invoice_form.html', {
        'form': form,
        'title': title,
        'fee_plans': fee_plans,
        'back_url': back_url
    })

@coach_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('student', 'fee_plan'), pk=pk)
    payments = invoice.payments.all()
    reminders = invoice.reminders.all()
    return render(request, 'fees/invoice_detail.html', {
        'invoice': invoice,
        'payments': payments,
        'reminders': reminders,
    })

@coach_required
@require_POST
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    messages.success(request, 'Invoice deleted.')
    return redirect('fees:invoice_list')

@coach_required
def record_payment(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()  # This will update invoice amount_paid and status
            messages.success(request, 'Payment recorded successfully.')
            return redirect('fees:invoice_detail', pk=invoice.pk)
    else:
        form = PaymentForm(initial={'amount': invoice.balance, 'payment_date': timezone.now().date()})
        
    return render(request, 'fees/payment_form.html', {
        'form': form,
        'invoice': invoice,
        'title': 'Record Payment',
        'back_url': 'fees:invoice_detail'
    })

@coach_required
def payment_list(request):
    payments = Payment.objects.select_related('invoice__student').all()
    date_filter = request.GET.get('date')
    if date_filter:
        payments = payments.filter(payment_date=date_filter)
        
    return render(request, 'fees/payment_list.html', {
        'items': payments,
        'date_filter': date_filter
    })

@coach_required
def reminder_list(request):
    reminders = PaymentReminder.objects.select_related('invoice__student').all()
    return render(request, 'fees/reminder_list.html', {
        'items': reminders
    })

@coach_required
def create_reminder(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    settings = SiteSettings.load()
    
    parent = invoice.student.parents.first()
    parent_name = parent.name if parent else 'Parent'
    
    default_message = settings.fee_reminder_template.format(
        parent_name=parent_name,
        amount=invoice.balance,
        student_name=invoice.student.full_name,
        due_date=invoice.due_date.strftime('%d %b %Y')
    )
    
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.invoice = invoice
            reminder.save()
            messages.success(request, 'Reminder created successfully.')
            return redirect('fees:invoice_detail', pk=invoice.pk)
    else:
        form = ReminderForm(initial={
            'scheduled_date': timezone.now().date(),
            'message': default_message,
        })
        
    return render(request, 'fees/reminder_form.html', {
        'form': form,
        'invoice': invoice,
        'title': 'Create Reminder',
        'back_url': 'fees:invoice_detail'
    })

@coach_required
@require_POST
def cancel_reminder(request, pk):
    reminder = get_object_or_404(PaymentReminder, pk=pk)
    reminder.status = 'cancelled'
    reminder.save()
    messages.success(request, 'Reminder cancelled.')
    return redirect('fees:reminder_list')

@coach_required
def whatsapp_reminder(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    settings = SiteSettings.load()
    parent = invoice.student.parents.first()
    parent_name = parent.name if parent else 'Parent'
    whatsapp_num = parent.whatsapp if parent else ''
    
    message = settings.fee_reminder_template.format(
        parent_name=parent_name,
        amount=invoice.balance,
        student_name=invoice.student.full_name,
        due_date=invoice.due_date.strftime('%d %b %Y')
    )
    
    wa_url = f'https://wa.me/{whatsapp_num.replace("+","").replace(" ","")}?text={urllib.parse.quote(message)}'
    
    # Optional: Log the reminder
    PaymentReminder.objects.create(
        invoice=invoice,
        reminder_type='whatsapp',
        scheduled_date=timezone.now().date(),
        message=message,
        status='sent',
        sent_at=timezone.now()
    )
    
    return redirect(wa_url)
