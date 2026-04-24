from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChurchGroup, GroupMembership
from members.models import MemberProfile

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
        messages.warning(request, "You need to be an approved member to join groups. 🙏")
        return redirect('dashboard')
    return wrapper

def group_list(request):
    groups = ChurchGroup.objects.filter(is_active=True)
    my_groups = []
    if request.user.is_authenticated:
        my_groups = list(GroupMembership.objects.filter(member=request.user, is_active=True).values_list('group_id', flat=True))
    return render(request, 'groups/group_list.html', {'groups':groups,'my_groups':my_groups})

def group_detail(request, pk):
    group = get_object_or_404(ChurchGroup, pk=pk)
    memberships = group.memberships.filter(is_active=True).select_related('member')
    meetings = group.meetings.all()[:5]
    is_member = False
    if request.user.is_authenticated:
        is_member = GroupMembership.objects.filter(group=group, member=request.user, is_active=True).exists()
    return render(request, 'groups/group_detail.html', {'group':group,'memberships':memberships,'meetings':meetings,'is_member':is_member})

@approved_required
def join_group(request, pk):
    group = get_object_or_404(ChurchGroup, pk=pk)
    membership, created = GroupMembership.objects.get_or_create(group=group, member=request.user, defaults={'role':'member','is_active':True})
    if created:
        messages.success(request, f"You have joined {group.name}! 🙏")
    elif not membership.is_active:
        membership.is_active = True
        membership.save()
        messages.success(request, f"Welcome back to {group.name}!")
    else:
        messages.info(request, f"You are already a member of {group.name}.")
    return redirect('group_detail', pk=pk)

@approved_required
def leave_group(request, pk):
    group = get_object_or_404(ChurchGroup, pk=pk)
    membership = GroupMembership.objects.filter(group=group, member=request.user, is_active=True).first()
    if membership:
        membership.is_active = False
        membership.save()
        messages.success(request, f"You have left {group.name}. You can rejoin at any time.")
    return redirect('group_list')

@login_required
def my_groups(request):
    memberships = GroupMembership.objects.filter(member=request.user, is_active=True).select_related('group')
    return render(request, 'groups/my_groups.html', {'memberships': memberships})
