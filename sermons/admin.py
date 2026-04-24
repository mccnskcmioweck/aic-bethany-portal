from django.contrib import admin
from django.utils.html import format_html
from .models import Sermon, Announcement

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_preacher_name', 'scripture_reference', 'sermon_date', 'series', 'media_links']
    list_filter = ['sermon_date', 'series']
    search_fields = ['title', 'scripture_reference', 'preacher_name']
    fieldsets = (
        ('📖 Sermon Details', {
            'fields': ('title', 'preacher', 'preacher_name', 'scripture_reference', 'sermon_date', 'series', 'summary')
        }),
        ('🎬 Video Links', {
            'fields': ('youtube_url', 'facebook_url'),
            'description': 'Paste the full video URL from YouTube or Facebook.'
        }),
        ('🎵 Audio & Notes', {
            'fields': ('audio_file', 'notes_pdf'),
            'classes': ('collapse',)
        }),
    )

    def media_links(self, obj):
        links = []
        if obj.youtube_url:
            links.append(format_html('<a href="{}" target="_blank" style="color:red"><i>▶ YouTube</i></a>', obj.youtube_url))
        if obj.facebook_url:
            links.append(format_html('<a href="{}" target="_blank" style="color:#1877f2"><i>f Facebook</i></a>', obj.facebook_url))
        if obj.audio_file:
            links.append(format_html('<span style="color:green">🎵 Audio</span>'))
        return format_html(' &nbsp; '.join(links)) if links else format_html('<span style="color:#aaa">None</span>')
    media_links.short_description = 'Media'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_active', 'start_date', 'end_date']
    list_filter = ['priority', 'is_active']
