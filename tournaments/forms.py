from django import forms
from .models import TournamentResult

class TournamentResultForm(forms.ModelForm):
    class Meta:
        model = TournamentResult
        exclude = ['created_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'highlights': forms.Textarea(attrs={'rows': 3}),
            'coach_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.DateInput)):
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')
