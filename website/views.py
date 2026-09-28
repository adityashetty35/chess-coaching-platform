from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import SiteSettings, CoachingService, CoachingProgram, Testimonial, FAQ, Achievement
from .forms import PublicEnquiryForm

def home(request):
    context = {
        'site_settings': SiteSettings.objects.first(),
        'services': CoachingService.objects.filter(is_active=True).order_by('order'),
        'programs': CoachingProgram.objects.filter(is_active=True).order_by('order'),
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('order'),
        'faqs': FAQ.objects.filter(is_active=True).order_by('order'),
        'achievements': Achievement.objects.filter(is_active=True).order_by('order'),
    }
    # For models that might not have is_active or order, fallback
    try:
        context['services'] = CoachingService.objects.filter(is_active=True)
    except:
        context['services'] = CoachingService.objects.all()
        
    try:
        context['programs'] = CoachingProgram.objects.filter(is_active=True)
    except:
        context['programs'] = CoachingProgram.objects.all()
        
    try:
        context['testimonials'] = Testimonial.objects.filter(is_active=True)
    except:
        context['testimonials'] = Testimonial.objects.all()
        
    try:
        context['faqs'] = FAQ.objects.filter(is_active=True)
    except:
        context['faqs'] = FAQ.objects.all()
        
    try:
        context['achievements'] = Achievement.objects.filter(is_active=True)
    except:
        context['achievements'] = Achievement.objects.all()

    return render(request, 'website/home.html', context)

def enquiry_form(request):
    if request.method == 'POST':
        form = PublicEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('website:enquiry_thank_you')
    else:
        form = PublicEnquiryForm()
    
    context = {
        'form': form,
        'site_settings': SiteSettings.objects.first(),
    }
    return render(request, 'website/enquiry.html', context)

def enquiry_thank_you(request):
    context = {
        'site_settings': SiteSettings.objects.first(),
    }
    return render(request, 'website/enquiry_thank_you.html', context)
