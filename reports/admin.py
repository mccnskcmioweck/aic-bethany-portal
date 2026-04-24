from django.contrib import admin
from .models import AttendanceReport, SundaySchoolReport, OfferingReport, SpiritualProgramReport
@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ['date','service_type','total_attendance','visitors','new_converts']
    list_filter = ['service_type']
    date_hierarchy = 'date'
@admin.register(SundaySchoolReport)
class SundaySchoolReportAdmin(admin.ModelAdmin):
    list_display = ['date','lesson_topic','teacher','total_students','teachers_present']
    date_hierarchy = 'date'
@admin.register(OfferingReport)
class OfferingReportAdmin(admin.ModelAdmin):
    list_display = ['date','service_type','grand_total','currency','verified_by']
    list_filter = ['service_type']
    date_hierarchy = 'date'
@admin.register(SpiritualProgramReport)
class SpiritualProgramReportAdmin(admin.ModelAdmin):
    list_display = ['date','program_type','title','members_present','total_members']
    list_filter = ['program_type']
    date_hierarchy = 'date'
