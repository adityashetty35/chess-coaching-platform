from django import forms
from .models import ProgressEntry, Goal

class ProgressEntryForm(forms.ModelForm):
    class Meta:
        model = ProgressEntry
        exclude = ['student', 'created_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'rating': forms.NumberInput(attrs={'min': 0}),
            'tactics': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'opening_knowledge': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'middlegame': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'endgame': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'calculation': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'positional': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'time_management': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'strengths': forms.Textarea(attrs={'rows': 3}),
            'weaknesses': forms.Textarea(attrs={'rows': 3}),
            'next_goals': forms.Textarea(attrs={'rows': 3}),
            'coach_comments': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.DateInput)):
                field.widget.attrs.setdefault('class', 'form-control')

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        exclude = ['student', 'created_at', 'updated_at']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'coach_notes': forms.Textarea(attrs={'rows': 3}),
            'progress_percent': forms.NumberInput(attrs={'min': 0, 'max': 100}),
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
