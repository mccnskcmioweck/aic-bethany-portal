from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import MemberProfile, ServiceRequest, ChurchPosition

admin.site.site_header = "🙏 AIC Bethany – Admin Panel"
admin.site.site_title = "AIC Bethany Portal"
admin.site.index_title = "Church Administration Dashboard"

@admin.register(ChurchPosition)
class ChurchPositionAdmin(admin.ModelAdmin):
    list_display = ['name','category','order','holder_count']
    list_filter = ['category']
    list_editable = ['order']
    def holder_count(self, obj):
        count = obj.holders.filter(status='active').count()
        color = 'green' if count else '#999'
        return format_html('<span style="color:{};font-weight:bold">{}</span>', color, count)
    holder_count.short_description = "Active Holders"

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ['photo_thumb','full_name','phone','position_badge','status_badge','created_at']
    list_filter = ['status','position','gender']
    search_fields = ['user__first_name','user__last_name','user__email','phone']
    readonly_fields = ['created_at','approved_at','approved_by','photo_thumb']
    list_per_page = 20
    actions = ['approve_members','suspend_members']
    fieldsets = (
        ('👤 Personal Information', {'fields': ('user','photo','photo_thumb','gender','date_of_birth','phone','address')}),
        ('⛪ Church Details', {'fields': ('position','status','date_joined_church','baptism_date','bio')}),
        ('🚨 Emergency Contact', {'fields': ('emergency_contact_name','emergency_contact_phone'),'classes': ('collapse',)}),
        ('📋 Admin Notes', {'fields': ('admin_notes',),'classes': ('collapse',)}),
        ('✅ Approval Info', {'fields': ('approved_by','approved_at','created_at'),'classes': ('collapse',)}),
    )
    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;">',obj.photo.url)
        initials = (obj.user.first_name[:1]+obj.user.last_name[:1]).upper() or '?'
        return format_html('<div style="width:40px;height:40px;border-radius:50%;background:#1a3c6e;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:14px">{}</div>',initials)
    photo_thumb.short_description = ''
    def full_name(self, obj):
        return format_html('<strong>{}</strong><br><small style="color:#888">{}</small>',obj.user.get_full_name() or obj.user.username,obj.user.email)
    full_name.short_description = 'Member'
    def position_badge(self, obj):
        if obj.position:
            return format_html('<span style="background:#1a3c6e;color:white;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',obj.position.name)
        return format_html('<span style="color:#aaa;font-size:11px">Member</span>')
    position_badge.short_description = 'Position'
    def status_badge(self, obj):
        colors = {'active':('#28a745','✅ Active'),'pending':('#ffc107','⏳ Pending'),'inactive':('#6c757d','💤 Inactive'),'suspended':('#dc3545','🚫 Suspended')}
        color, label = colors.get(obj.status,('#999',obj.status))
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',color,label)
    status_badge.short_description = 'Status'
    def approve_members(self, request, queryset):
        count = queryset.filter(status='pending').count()
        queryset.filter(status='pending').update(status='active',approved_by=request.user,approved_at=timezone.now())
        self.message_user(request,f"✅ {count} member(s) approved.")
    approve_members.short_description = "✅ Approve selected members"
    def suspend_members(self, request, queryset):
        queryset.update(status='suspended')
        self.message_user(request,f"🚫 {queryset.count()} member(s) suspended.")
    suspend_members.short_description = "🚫 Suspend selected members"

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['subject','member_name','request_type_badge','status_badge','assigned_to','created_at']
    list_filter = ['request_type','status']
    search_fields = ['subject','member__first_name','member__last_name']
    readonly_fields = ['created_at','updated_at']
    list_per_page = 20
    fieldsets = (
        ('📋 Request Details', {'fields': ('member','request_type','subject','description','preferred_date')}),
        ('⚙️ Management', {'fields': ('status','assigned_to','admin_notes')}),
        ('🕐 Timestamps', {'fields': ('created_at','updated_at'),'classes': ('collapse',)}),
    )
    def member_name(self, obj):
        return format_html('<strong>{}</strong><br><small style="color:#888">{}</small>',obj.member.get_full_name() or obj.member.username,obj.member.email)
    member_name.short_description = 'Member'
    def request_type_badge(self, obj):
        return format_html('<span style="background:#6c757d;color:white;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',obj.get_request_type_display())
    request_type_badge.short_description = 'Type'
    def status_badge(self, obj):
        colors = {'pending':('#ffc107','⏳ Pending'),'assigned':('#17a2b8','👤 Assigned'),'completed':('#28a745','✅ Completed'),'cancelled':('#dc3545','❌ Cancelled')}
        color, label = colors.get(obj.status,('#999',obj.status))
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',color,label)
    status_badge.short_description = 'Status'
