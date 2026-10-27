from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import IntegrationSettings, UserRole, WhatsAppTemplate, ReminderSchedule
from .permissions import MODULES, DEFAULT_ADMIN
from students.models import Parent


class ManagedUserForm(forms.ModelForm):
    parent_profile = forms.ModelChoiceField(queryset=Parent.objects.all(), required=False,
                                           help_text='For Parent role, link an existing parent record to enable their portal and OTP login.')
    role = forms.ChoiceField(choices=UserRole.ROLE_CHOICES)
    permissions = forms.MultipleChoiceField(
        choices=[(key, key.replace('_', ' ').title()) for key in MODULES],
        required=False, widget=forms.CheckboxSelectMultiple,
        help_text='Only applies to Academy Admin; Coaches receive fixed, assigned-class access.')
    password = forms.CharField(required=False, widget=forms.PasswordInput,
                               help_text='Required for new users. Leave empty when editing to keep the password.')

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            record = UserRole.objects.filter(user=self.instance).first()
            self.fields['role'].initial = record.role if record else (
                UserRole.SUPER_ADMIN if self.instance.is_superuser else
                UserRole.ACADEMY_ADMIN if self.instance.is_staff else UserRole.PARENT)
            self.fields['permissions'].initial = record.permissions if record else DEFAULT_ADMIN
            self.fields['parent_profile'].initial = Parent.objects.filter(user=self.instance).first()
        else:
            self.fields['role'].initial = UserRole.PARENT
            self.fields['is_active'].initial = True
        for name, field in self.fields.items():
            if name not in ('permissions', 'is_active'):
                field.widget.attrs.setdefault('class', 'form-select' if name == 'role' else 'form-control')

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.instance.pk and not password:
            raise forms.ValidationError('A password is required for a new user.')
        if password:
            validate_password(password, user=self.instance)
        return password

    def clean(self):
        values = super().clean()
        if self.instance.pk and self.instance.is_superuser and (
                values.get('role') != UserRole.SUPER_ADMIN or not values.get('is_active')):
            from django.contrib.auth import get_user_model
            if get_user_model().objects.filter(is_superuser=True, is_active=True).count() <= 1:
                raise forms.ValidationError('You cannot remove the final active Super Administrator.')
        parent = values.get('parent_profile')
        if parent and parent.user_id and parent.user_id != self.instance.pk:
            self.add_error('parent_profile', 'This parent profile is already linked to another user.')
        return values


class IntegrationForm(forms.ModelForm):
    class Meta:
        model = IntegrationSettings
        exclude = ['id']
        widgets = {
            'whatsapp_template': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'


class WhatsAppTemplateForm(forms.ModelForm):
    class Meta:
        model = WhatsAppTemplate
        fields = ['name', 'content_sid', 'preview_text', 'is_active']
        widgets = {'preview_text': forms.Textarea(attrs={'rows': 3})}

    def clean_content_sid(self):
        sid = self.cleaned_data['content_sid'].strip()
        if not sid.startswith('HX') or len(sid) != 34:
            raise forms.ValidationError('Use a valid Twilio Content SID starting with HX.')
        return sid


class ReminderScheduleForm(forms.ModelForm):
    class Meta:
        model = ReminderSchedule
        fields = ['name', 'days_offset', 'template', 'is_active']

    def clean_days_offset(self):
        value = self.cleaned_data['days_offset']
        if not -60 <= value <= 60:
            raise forms.ValidationError('Choose a date within 60 days of the invoice due date.')
        return value
