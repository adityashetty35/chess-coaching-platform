from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def coach_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('portal:dashboard')
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
