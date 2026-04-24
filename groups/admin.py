from django.contrib import admin
from .models import ChurchGroup, GroupMembership, GroupMeeting
@admin.register(ChurchGroup)
class ChurchGroupAdmin(admin.ModelAdmin):
    list_display = ['name','group_type','leader','member_count','is_active']
    list_filter = ['group_type','is_active']
@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['member','group','role','is_active','date_joined']
    list_filter = ['group','role','is_active']
@admin.register(GroupMeeting)
class GroupMeetingAdmin(admin.ModelAdmin):
    list_display = ['group','date','attendance_count','recorded_by']
