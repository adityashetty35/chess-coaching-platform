from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import UserRole

MODULES = ('dashboard', 'enquiries', 'students', 'lessons', 'attendance', 'batches', 'fees', 'progress', 'homework')
DEFAULT_ADMIN = list(MODULES)
COACH_MODULES = {'dashboard', 'lessons', 'attendance', 'progress', 'homework'}


def role_for(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return UserRole.SUPER_ADMIN
    record = UserRole.objects.filter(user=user).first()
    if record:
        return UserRole.ACADEMY_ADMIN if record.role == UserRole.SUPER_ADMIN else record.role
    return UserRole.ACADEMY_ADMIN if user.is_staff else UserRole.PARENT


def has_module(user, module):
    if not user.is_authenticated or not user.is_active:
        return False
    role = role_for(user)
    if role == UserRole.SUPER_ADMIN:
        return True
    if role == UserRole.COACH:
        return module in COACH_MODULES
    if role == UserRole.ACADEMY_ADMIN:
        record = UserRole.objects.filter(user=user).first()
        return module in (record.permissions if record else DEFAULT_ADMIN)
    return False


def ensure_assigned_student(user, student_id):
    if role_for(user) != UserRole.COACH:
        return
    from coaching.models import ChessClass
    if not ChessClass.objects.filter(assigned_coach=user).filter(
        Q(students__id=student_id) | Q(batch__students__id=student_id)
    ).exists():
        raise PermissionDenied('This student is not assigned to you.')
