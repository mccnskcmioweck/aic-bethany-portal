from django.db import models
from django.contrib.auth.models import User

class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    preacher_name = models.CharField(max_length=100, blank=True)
    scripture_reference = models.CharField(max_length=200)
    sermon_date = models.DateField()
    summary = models.TextField()
    audio_file = models.FileField(upload_to='sermons/audio/', null=True, blank=True)
    youtube_url = models.URLField(blank=True, verbose_name="YouTube Link",
        help_text="Paste the full YouTube video URL e.g. https://www.youtube.com/watch?v=XXXXX")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook Link",
        help_text="Paste the full Facebook video URL e.g. https://www.facebook.com/watch?v=XXXXX")
    notes_pdf = models.FileField(upload_to='sermons/notes/', null=True, blank=True)
    series = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sermon_date']

    def __str__(self):
        return f"{self.title} - {self.sermon_date}"

    def get_preacher_name(self):
        if self.preacher:
            return self.preacher.get_full_name() or self.preacher.username
        return self.preacher_name or "Unknown"

    def get_youtube_embed(self):
        """Convert YouTube watch URL to embed URL"""
        if not self.youtube_url:
            return None
        url = self.youtube_url
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
        elif 'watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
        else:
            return None
        return f"https://www.youtube.com/embed/{video_id}"


class Announcement(models.Model):
    PRIORITY_CHOICES = [('low','Low'),('normal','Normal'),('high','High'),('urgent','Urgent')]
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority','-created_at']

    def __str__(self):
        return self.title
