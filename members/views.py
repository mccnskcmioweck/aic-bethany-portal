from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django import forms
from .models import MemberProfile, ServiceRequest, ChurchPosition

def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Administrators only.")
        return redirect('dashboard')
    return wrapper

def approved_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        try:
            if request.user.profile.is_approved():
                return view_func(request, *args, **kwargs)
        except MemberProfile.DoesNotExist:
            pass
        messages.warning(request, "Your account is pending admin approval. You will gain full access once approved. 🙏")
        return redirect('dashboard')
    return wrapper

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone','password1','password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            MemberProfile.objects.create(user=user, phone=self.cleaned_data.get('phone',''), status='pending')
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['phone','gender','date_of_birth','address','photo','bio','baptism_date','emergency_contact_name','emergency_contact_phone']
        widgets = {'date_of_birth':forms.DateInput(attrs={'type':'date'}),'baptism_date':forms.DateInput(attrs={'type':'date'}),'bio':forms.Textarea(attrs={'rows':3}),'address':forms.Textarea(attrs={'rows':2})}

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['request_type','subject','description','preferred_date']
        widgets = {'preferred_date':forms.DateInput(attrs={'type':'date'}),'description':forms.Textarea(attrs={'rows':4})}

class AdminRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status','assigned_to','admin_notes']
        widgets = {'admin_notes':forms.Textarea(attrs={'rows':3})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=True)
        self.fields['assigned_to'].required = False

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration submitted! Your account is pending admin approval. You will receive access once approved. 🙏")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'members/register.html', {'form': form})

@approved_required
def profile(request):
    try:
        member_profile = request.user.profile
    except MemberProfile.DoesNotExist:
        member_profile = MemberProfile.objects.create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=member_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=member_profile)
    return render(request, 'members/profile.html', {'form':form,'member_profile':member_profile})

@approved_required
def service_request_create(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            sr = form.save(commit=False)
            sr.member = request.user
            sr.save()
            messages.success(request, "Your request has been submitted. The admin will respond soon. 🙏")
            return redirect('my_requests')
    else:
        form = ServiceRequestForm()
    return render(request, 'members/service_request_form.html', {'form': form})

@login_required
def my_requests(request):
    requests_list = ServiceRequest.objects.filter(member=request.user)
    return render(request, 'members/my_requests.html', {'requests_list': requests_list})

@admin_required
def member_list(request):
    status_filter = request.GET.get('status','')
    members = MemberProfile.objects.select_related('user','position').all()
    if status_filter:
        members = members.filter(status=status_filter)
    counts = {'all':MemberProfile.objects.count(),'active':MemberProfile.objects.filter(status='active').count(),'pending':MemberProfile.objects.filter(status='pending').count(),'inactive':MemberProfile.objects.filter(status='inactive').count(),'suspended':MemberProfile.objects.filter(status='suspended').count()}
    return render(request, 'members/member_list.html', {'members':members,'counts':counts,'status_filter':status_filter})

@admin_required
def member_detail(request, pk):
    mp = get_object_or_404(MemberProfile, pk=pk)
    requests_list = ServiceRequest.objects.filter(member=mp.user)
    return render(request, 'members/member_detail.html', {'member_profile':mp,'requests_list':requests_list})

@admin_required
def member_edit(request, pk):
    mp = get_object_or_404(MemberProfile, pk=pk)
    if request.method == 'POST':
        mp.user.first_name = request.POST.get('first_name','')
        mp.user.last_name = request.POST.get('last_name','')
        mp.user.email = request.POST.get('email','')
        mp.user.save()
        mp.phone = request.POST.get('phone','')
        mp.gender = request.POST.get('gender','')
        mp.address = request.POST.get('address','')
        mp.admin_notes = request.POST.get('admin_notes','')
        mp.status = request.POST.get('status', mp.status)
        pos_id = request.POST.get('position','')
        mp.position = ChurchPosition.objects.filter(pk=pos_id).first() if pos_id else None
        dob = request.POST.get('date_of_birth','')
        mp.date_of_birth = dob if dob else None
        djc = request.POST.get('date_joined_church','')
        mp.date_joined_church = djc if djc else None
        bd = request.POST.get('baptism_date','')
        mp.baptism_date = bd if bd else None
        if mp.status == 'active' and not mp.approved_by:
            mp.approved_by = request.user
            mp.approved_at = timezone.now()
        mp.save()
        messages.success(request, f"{mp.user.get_full_name()} updated successfully! ✅")
        return redirect('member_detail', pk=pk)
    positions = ChurchPosition.objects.all()
    return render(request, 'members/member_edit.html', {'member_profile':mp,'positions':positions})

@admin_required
def approve_member(request, pk):
    mp = get_object_or_404(MemberProfile, pk=pk)
    mp.status = 'active'
    mp.approved_by = request.user
    mp.approved_at = timezone.now()
    mp.save()
    messages.success(request, f"✅ {mp.user.get_full_name()} approved! They now have full access.")
    return redirect('member_list')

@admin_required
def reject_member(request, pk):
    mp = get_object_or_404(MemberProfile, pk=pk)
    mp.status = 'suspended'
    mp.save()
    messages.warning(request, f"{mp.user.get_full_name()} registration rejected.")
    return redirect('member_list')

@admin_required
def request_list(request):
    status_filter = request.GET.get('status','')
    qs = ServiceRequest.objects.select_related('member','assigned_to').all()
    if status_filter:
        qs = qs.filter(status=status_filter)
    counts = {'all':ServiceRequest.objects.count(),'pending':ServiceRequest.objects.filter(status='pending').count(),'assigned':ServiceRequest.objects.filter(status='assigned').count(),'completed':ServiceRequest.objects.filter(status='completed').count()}
    return render(request, 'members/request_list.html', {'requests_qs':qs,'counts':counts,'status_filter':status_filter})

@admin_required
def request_manage(request, pk):
    sr = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        form = AdminRequestForm(request.POST, instance=sr)
        if form.is_valid():
            form.save()
            messages.success(request, "Request updated! ✅")
            return redirect('request_list')
    else:
        form = AdminRequestForm(instance=sr)
    return render(request, 'members/request_manage.html', {'form':form,'service_request':sr})
