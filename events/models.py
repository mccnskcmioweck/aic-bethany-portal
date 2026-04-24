from django.db import models
from django.contrib.auth.models import User
class Event(models.Model):
    CATEGORY_CHOICES = [('service','Church Service'),('prayer','Prayer Meeting'),('youth','Youth Program'),('women',"Women's Fellowship"),('men',"Men's Fellowship"),('outreach','Community Outreach'),('conference','Conference'),('other','Other')]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='service')
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=200)
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    class Meta:
        ordering = ['date','start_time']
    def __str__(self):
        return f"{self.title} - {self.date}"

class EventAttendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    class Meta:
        unique_together = ['event','member']
