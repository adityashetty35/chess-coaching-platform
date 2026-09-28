from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('core.auth_urls')),
    path('dashboard/', include('core.urls')),
    path('enquiries/', include('enquiries.urls')),
    path('students/', include('students.urls')),
    path('coaching/', include('coaching.urls')),
    path('fees/', include('fees.urls')),
    path('progress/', include('progress.urls')),
    path('assignments/', include('assignments.urls')),
    path('tournaments/', include('tournaments.urls')),
    path('announcements/', include('announcements.urls')),
    path('reports/', include('reports.urls')),
    path('portal/', include('portal.urls')),
    path('settings/', include('core.settings_urls')),
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
