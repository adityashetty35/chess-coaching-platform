from django import forms
from .models import ProgressEntry, Goal, SyllabusLesson, TestResult, FideRatingRecord, ScheduledTest


class ScheduledTestForm(forms.ModelForm):
    class Meta:
        model = ScheduledTest
        fields = ['title', 'level', 'date', 'batch', 'details']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class SyllabusLessonForm(forms.ModelForm):
    class Meta:
        model = SyllabusLesson
        fields = ['level', 'title', 'description', 'home_practice_url', 'order']


class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['student', 'title', 'test_date', 'score', 'max_score', 'coach_feedback', 'game_analysis']
        widgets = {'test_date': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        data = super().clean()
        if data.get('score') is not None and data.get('max_score') is not None:
            if data['max_score'] <= 0 or not 0 <= data['score'] <= data['max_score']:
                raise forms.ValidationError('Score must be between 0 and the positive maximum score.')
        return data


class FideRatingRecordForm(forms.ModelForm):
    class Meta:
        model = FideRatingRecord
        fields = ['student', 'recorded_on', 'rating', 'source_url']
        widgets = {'recorded_on': forms.DateInput(attrs={'type': 'date'})}

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
