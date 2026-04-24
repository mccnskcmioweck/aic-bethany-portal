from django.db import models
from django.contrib.auth.models import User
class ChurchGroup(models.Model):
    GROUP_TYPES = [('fellowship','Fellowship'),('spiritual','Spiritual Program'),('ministry','Ministry'),('other','Other')]
    name = models.CharField(max_length=200)
    group_type = models.CharField(max_length=20, choices=GROUP_TYPES, default='fellowship')
    description = models.TextField(blank=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_groups')
    co_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='co_led_groups')
    meeting_day = models.CharField(max_length=50, blank=True)
    meeting_time = models.TimeField(null=True, blank=True)
    meeting_venue = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def member_count(self):
        return self.memberships.filter(is_active=True).count()

class GroupMembership(models.Model):
    ROLE_CHOICES = [('member','Member'),('secretary','Secretary'),('treasurer','Treasurer'),('leader','Leader'),('patron','Patron')]
    group = models.ForeignKey(ChurchGroup, on_delete=models.CASCADE, related_name='memberships')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        unique_together = ['group','member']
    def __str__(self):
        return f"{self.member.get_full_name()} – {self.group.name}"

class GroupMeeting(models.Model):
    group = models.ForeignKey(ChurchGroup, on_delete=models.CASCADE, related_name='meetings')
    date = models.DateField()
    agenda = models.TextField(blank=True)
    minutes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
    def attendance_count(self):
        return self.attendances.filter(present=True).count()

class GroupAttendance(models.Model):
    meeting = models.ForeignKey(GroupMeeting, on_delete=models.CASCADE, related_name='attendances')
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(default=True)
    class Meta:
        unique_together = ['meeting','member']
