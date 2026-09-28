from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.decorators import coach_required
from .models import TournamentResult
from .forms import TournamentResultForm

@coach_required
def tournament_list(request):
    results = TournamentResult.objects.all().select_related('student__user')
    return render(request, 'tournaments/list.html', {
        'results': results,
        'title': 'Tournament Results'
    })

@coach_required
def tournament_form(request, pk=None):
    result = get_object_or_404(TournamentResult, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = TournamentResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tournament result saved.')
            return redirect('tournaments:list')
    else:
        form = TournamentResultForm(instance=result)
        
    return render(request, 'tournaments/form.html', {
        'form': form,
        'title': 'Edit Tournament Result' if pk else 'Add Tournament Result'
    })

@require_POST
@coach_required
def tournament_delete(request, pk):
    result = get_object_or_404(TournamentResult, pk=pk)
    result.delete()
    messages.success(request, 'Tournament result deleted.')
    return redirect('tournaments:list')
