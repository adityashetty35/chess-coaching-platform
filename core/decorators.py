from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .permissions import has_module, role_for
from .models import UserRole

APP_MODULE = {'core': 'dashboard', 'enquiries': 'enquiries', 'students': 'students',
              'coaching': 'lessons', 'fees': 'fees', 'progress': 'progress', 'assignments': 'homework'}

def coach_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        app = view_func.__module__.split('.')[0]
        module = APP_MODULE.get(app)
        if app == 'core' and view_func.__name__ != 'dashboard':
            if not request.user.is_superuser:
                raise PermissionDenied('Only the Super Administrator can change academy settings.')
        elif app == 'coaching' and view_func.__name__.startswith('batch_'):
            if not has_module(request.user, 'batches'):
                raise PermissionDenied()
        elif app == 'coaching' and view_func.__name__ == 'mark_attendance':
            if not has_module(request.user, 'attendance'):
                raise PermissionDenied()
        elif app == 'coaching' and view_func.__name__ in ('class_list', 'class_detail', 'calendar_view', 'calendar_events'):
            if not (has_module(request.user, 'lessons') or has_module(request.user, 'attendance')):
                raise PermissionDenied()
        elif not module or not has_module(request.user, module):
            if role_for(request.user) == UserRole.PARENT:
                return redirect('portal:dashboard')
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'student_profile'):
            return redirect('portal:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def parent_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'parent_profile'):
            return redirect('portal:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
