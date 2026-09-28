from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.decorators import coach_required
from .models import Announcement
from .forms import AnnouncementForm

@coach_required
def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'announcements/list.html', {
        'announcements': announcements,
        'title': 'Announcements'
    })

@coach_required
def announcement_form(request, pk=None):
    announcement = get_object_or_404(Announcement, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement saved.')
            return redirect('announcements:list')
    else:
        form = AnnouncementForm(instance=announcement)
        
    return render(request, 'announcements/form.html', {
        'form': form,
        'title': 'Edit Announcement' if pk else 'Add Announcement'
    })

@coach_required
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'announcements/detail.html', {
        'announcement': announcement,
        'title': announcement.title
    })

@require_POST
@coach_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    messages.success(request, 'Announcement deleted.')
    return redirect('announcements:list')
