from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from members.models import MemberProfile, ServiceRequest
from events.models import Event
from sermons.models import Sermon, Announcement

def home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date(), is_public=True)[:3]
    recent_sermons = Sermon.objects.all()[:3]
    announcements = Announcement.objects.filter(is_active=True, start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date())
    return render(request, 'core/home.html', {'upcoming_events':upcoming_events,'recent_sermons':recent_sermons,'announcements':announcements})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}! 🙏")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out. God bless you!")
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    try:
        profile = user.profile
    except MemberProfile.DoesNotExist:
        profile = None
    my_requests = ServiceRequest.objects.filter(member=user)[:5]
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date())[:5]
    announcements = Announcement.objects.filter(is_active=True, start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date())
    context = {'profile':profile,'my_requests':my_requests,'upcoming_events':upcoming_events,'announcements':announcements}
    if user.is_staff:
        context['total_members'] = MemberProfile.objects.filter(status='active').count()
        context['pending_members'] = MemberProfile.objects.filter(status='pending').count()
        context['pending_requests'] = ServiceRequest.objects.filter(status='pending').count()
    return render(request, 'core/dashboard.html', context)
