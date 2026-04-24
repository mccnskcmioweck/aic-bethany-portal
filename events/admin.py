from django.contrib import admin
from .models import Event, EventAttendance
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title','category','date','start_time','venue','is_public']
    list_filter = ['category','is_public']
@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ['event','member','registered_at','attended']
