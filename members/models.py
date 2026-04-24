from django.db import models
from django.contrib.auth.models import User

class ChurchPosition(models.Model):
    CATEGORY_CHOICES = [('leadership','Church Leadership'),('committee','Committee'),('ministry','Ministry Head'),('other','Other')]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='leadership')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'name']
    def __str__(self):
        return self.name

class MemberProfile(models.Model):
    STATUS_CHOICES = [('pending','Pending Approval'),('active','Active'),('inactive','Inactive'),('suspended','Suspended')]
    GENDER_CHOICES = [('M','Male'),('F','Female')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='member_photos/', null=True, blank=True)
    position = models.ForeignKey(ChurchPosition, null=True, blank=True, on_delete=models.SET_NULL, related_name='holders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_joined_church = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    baptism_date = models.DateField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_members')
    approved_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
    def is_approved(self):
        return self.status == 'active'
    def display_position(self):
        return self.position.name if self.position else 'Member'

class ServiceRequest(models.Model):
    REQUEST_TYPES = [('prayer','Prayer Request'),('counseling','Counseling'),('home_visit','Home Visit'),('baptism','Baptism'),('wedding','Wedding Ceremony'),('funeral','Funeral Service'),('dedication','Child Dedication'),('other','Other')]
    STATUS_CHOICES = [('pending','Pending'),('assigned','Assigned'),('completed','Completed'),('cancelled','Cancelled')]
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    request_type = models.CharField(max_length=30, choices=REQUEST_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    preferred_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_requests')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.get_request_type_display()} - {self.member.get_full_name()}"
