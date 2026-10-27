from core.models import SiteSettings
from core.permissions import has_module

def site_settings(request):
    try:
        settings = SiteSettings.load()
    except Exception:
        settings = None
    available = {}
    if request.user.is_authenticated:
        available = {module: has_module(request.user, module) for module in (
            'dashboard', 'enquiries', 'students', 'lessons', 'attendance', 'batches', 'fees', 'progress', 'homework')}
    return {'site_settings': settings, 'academy_access': available}
