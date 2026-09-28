from django import forms
from .models import FeePlan, Invoice, Payment, PaymentReminder
from students.models import Student

class BaseFormClass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')
                field.widget.attrs.setdefault('rows', 3)
            elif isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.DateInput, forms.TimeInput)):
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.setdefault('class', 'form-select')
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-check-input')
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.setdefault('class', 'form-control')

class FeePlanForm(BaseFormClass):
    class Meta:
        model = FeePlan
        fields = ['name', 'description', 'amount', 'frequency', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class InvoiceForm(BaseFormClass):
    class Meta:
        model = Invoice
        fields = ['student', 'fee_plan', 'description', 'amount', 'due_date', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(status='active').order_by('first_name')
        self.fields['fee_plan'].queryset = FeePlan.objects.filter(is_active=True)

class PaymentForm(BaseFormClass):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'method', 'reference', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class ReminderForm(BaseFormClass):
    class Meta:
        model = PaymentReminder
        fields = ['scheduled_date', 'reminder_type', 'message']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 5}),
        }
