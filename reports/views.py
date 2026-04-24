from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from datetime import date, timedelta
from .models import AttendanceReport, SundaySchoolReport, OfferingReport, SpiritualProgramReport

def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    return wrapper

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceReport
        exclude = ['recorded_by','created_at']
        widgets = {'date':forms.DateInput(attrs={'type':'date'}),'notes':forms.Textarea(attrs={'rows':3})}

class SundaySchoolForm(forms.ModelForm):
    class Meta:
        model = SundaySchoolReport
        exclude = ['recorded_by','created_at']
        widgets = {'date':forms.DateInput(attrs={'type':'date'}),'lesson_summary':forms.Textarea(attrs={'rows':3}),'remarks':forms.Textarea(attrs={'rows':2})}

class OfferingForm(forms.ModelForm):
    class Meta:
        model = OfferingReport
        exclude = ['recorded_by','created_at']
        widgets = {'date':forms.DateInput(attrs={'type':'date'}),'notes':forms.Textarea(attrs={'rows':3})}

class SpiritualProgramForm(forms.ModelForm):
    class Meta:
        model = SpiritualProgramReport
        exclude = ['recorded_by','created_at']
        widgets = {'date':forms.DateInput(attrs={'type':'date'}),'activity_summary':forms.Textarea(attrs={'rows':3}),'achievements':forms.Textarea(attrs={'rows':2}),'prayer_items':forms.Textarea(attrs={'rows':2}),'upcoming_plans':forms.Textarea(attrs={'rows':2}),'remarks':forms.Textarea(attrs={'rows':2})}

@admin_required
def report_dashboard(request):
    today = date.today()
    month_start = today.replace(day=1)
    monthly_attendance = AttendanceReport.objects.filter(date__gte=month_start)
    total_this_month = sum(r.total_attendance for r in monthly_attendance)
    monthly_offering = OfferingReport.objects.filter(date__gte=month_start)
    total_offering_month = sum(r.grand_total() for r in monthly_offering)
    return render(request, 'reports/dashboard.html', {'total_this_month':total_this_month,'total_offering_month':total_offering_month,'attendance_records':AttendanceReport.objects.count(),'recent_attendance':AttendanceReport.objects.all()[:5],'recent_offerings':OfferingReport.objects.all()[:5],'recent_programs':SpiritualProgramReport.objects.all()[:5]})

@admin_required
def attendance_list(request):
    return render(request, 'reports/attendance_list.html', {'records': AttendanceReport.objects.all()})

@admin_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.recorded_by = request.user
            if not obj.total_attendance:
                obj.total_attendance = obj.men+obj.women+obj.youth+obj.children
            obj.save()
            messages.success(request, "Attendance report saved! ✅")
            return redirect('attendance_list')
    else:
        form = AttendanceForm(initial={'date':date.today()})
    return render(request, 'reports/form.html', {'form':form,'title':'Record Attendance','subtitle':'Fill in attendance figures for this service.','icon':'bi-people'})

@admin_required
def attendance_detail(request, pk):
    return render(request, 'reports/attendance_detail.html', {'record': get_object_or_404(AttendanceReport, pk=pk)})

@admin_required
def sunday_school_list(request):
    return render(request, 'reports/sunday_school_list.html', {'records': SundaySchoolReport.objects.all()})

@admin_required
def sunday_school_create(request):
    if request.method == 'POST':
        form = SundaySchoolForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False); obj.recorded_by = request.user; obj.save()
            messages.success(request, "Sunday School report saved! ✅")
            return redirect('sunday_school_list')
    else:
        form = SundaySchoolForm(initial={'date':date.today()})
    return render(request, 'reports/form.html', {'form':form,'title':'Sunday School Report','subtitle':'Record attendance and lesson details.','icon':'bi-book'})

@admin_required
def sunday_school_detail(request, pk):
    return render(request, 'reports/sunday_school_detail.html', {'record': get_object_or_404(SundaySchoolReport, pk=pk)})

@admin_required
def offering_list(request):
    today = date.today()
    month_records = OfferingReport.objects.filter(date__year=today.year, date__month=today.month)
    return render(request, 'reports/offering_list.html', {'records':OfferingReport.objects.all(),'monthly_total':sum(r.grand_total() for r in month_records),'monthly_tithes':sum(r.total_tithes() for r in month_records),'monthly_offering':sum(r.total_offering() for r in month_records)})

@admin_required
def offering_create(request):
    if request.method == 'POST':
        form = OfferingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False); obj.recorded_by = request.user; obj.save()
            messages.success(request, "Offering report saved! ✅")
            return redirect('offering_list')
    else:
        form = OfferingForm(initial={'date':date.today()})
    return render(request, 'reports/form.html', {'form':form,'title':'Offering & Tithes Report','subtitle':'Record all offerings and tithes for this service.','icon':'bi-cash-stack'})

@admin_required
def offering_detail(request, pk):
    return render(request, 'reports/offering_detail.html', {'record': get_object_or_404(OfferingReport, pk=pk)})

@admin_required
def program_list(request):
    return render(request, 'reports/program_list.html', {'records': SpiritualProgramReport.objects.all()})

@admin_required
def program_create(request):
    if request.method == 'POST':
        form = SpiritualProgramForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False); obj.recorded_by = request.user; obj.save()
            messages.success(request, "Program report saved! ✅")
            return redirect('program_list')
    else:
        form = SpiritualProgramForm(initial={'date':date.today()})
    return render(request, 'reports/form.html', {'form':form,'title':'Spiritual Program Report','subtitle':'Record choir, praise & worship, and ministry activities.','icon':'bi-music-note-beamed'})

@admin_required
def program_detail(request, pk):
    return render(request, 'reports/program_detail.html', {'record': get_object_or_404(SpiritualProgramReport, pk=pk)})
