from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, EventAttendance

def event_list(request):
    events = Event.objects.filter(date__gte=timezone.now().date(), is_public=True)
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventAttendance.objects.filter(event=event, member=request.user).exists()
    return render(request, 'events/event_detail.html', {'event':event,'is_registered':is_registered})

@login_required
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    attendance, created = EventAttendance.objects.get_or_create(event=event, member=request.user)
    if created:
        messages.success(request, f"You're registered for {event.title}! 🙏")
    else:
        messages.info(request, "You're already registered.")
    return redirect('event_detail', pk=pk)
