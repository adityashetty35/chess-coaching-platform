from django import forms
from enquiries.models import Enquiry

class PublicEnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            'student_name', 'parent_name', 'age', 'phone', 'whatsapp', 
            'email', 'current_level', 'current_rating', 'preferred_mode', 
            'preferred_schedule', 'coaching_goal', 'message'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'coaching_goal': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.DateInput, forms.TimeInput)):
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.setdefault('class', 'form-select')
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-check-input')
