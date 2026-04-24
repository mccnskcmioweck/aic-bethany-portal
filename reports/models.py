from django.db import models
from django.contrib.auth.models import User

class AttendanceReport(models.Model):
    SERVICE_TYPES = [('sunday_first','Sunday 1st Service'),('sunday_second','Sunday 2nd Service'),('sunday_evening','Sunday Evening Service'),('wednesday','Wednesday Bible Study'),('friday','Friday Prayer Meeting'),('special','Special Service'),('other','Other')]
    date = models.DateField()
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPES)
    total_attendance = models.PositiveIntegerField(default=0)
    men = models.PositiveIntegerField(default=0)
    women = models.PositiveIntegerField(default=0)
    youth = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)
    visitors = models.PositiveIntegerField(default=0)
    new_converts = models.PositiveIntegerField(default=0)
    presiding_minister = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='presided_services')
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_attendance')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
        unique_together = ['date','service_type']
    def __str__(self):
        return f"{self.get_service_type_display()} – {self.date}"

class SundaySchoolReport(models.Model):
    date = models.DateField(unique=True)
    lesson_topic = models.CharField(max_length=200)
    scripture_text = models.CharField(max_length=200, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='taught_sunday_school')
    nursery_class = models.PositiveIntegerField(default=0, verbose_name="Nursery (0–3 yrs)")
    junior_class = models.PositiveIntegerField(default=0, verbose_name="Junior (4–8 yrs)")
    middle_class = models.PositiveIntegerField(default=0, verbose_name="Middle (9–12 yrs)")
    senior_class = models.PositiveIntegerField(default=0, verbose_name="Senior (13–17 yrs)")
    teachers_present = models.PositiveIntegerField(default=0)
    memory_verse = models.CharField(max_length=300, blank=True)
    lesson_summary = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_sunday_school')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
    def total_students(self):
        return self.nursery_class + self.junior_class + self.middle_class + self.senior_class

class OfferingReport(models.Model):
    SERVICE_TYPES = [('sunday_first','Sunday 1st Service'),('sunday_second','Sunday 2nd Service'),('sunday_evening','Sunday Evening Service'),('wednesday','Wednesday Service'),('friday','Friday Service'),('special','Special Service / Harambee'),('other','Other')]
    date = models.DateField()
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPES)
    currency = models.CharField(max_length=5, default='KES')
    general_offering = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    thanksgiving_offering = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    special_offering = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    special_offering_purpose = models.CharField(max_length=200, blank=True)
    building_fund = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tithes_cash = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tithes_mpesa = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    missions_offering = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sunday_school_offering = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    counted_by = models.CharField(max_length=200, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_offerings')
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_offerings')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
    def total_offering(self):
        return self.general_offering+self.thanksgiving_offering+self.special_offering+self.building_fund+self.missions_offering+self.sunday_school_offering
    def total_tithes(self):
        return self.tithes_cash+self.tithes_mpesa
    def grand_total(self):
        return self.total_offering()+self.total_tithes()

class SpiritualProgramReport(models.Model):
    PROGRAM_TYPES = [('choir','Choir'),('praise_worship','Praise & Worship'),('drama','Drama Ministry'),('intercessory','Intercessory Prayer'),('evangelism','Evangelism Team'),('bible_study','Bible Study Group'),('other','Other')]
    program_type = models.CharField(max_length=30, choices=PROGRAM_TYPES)
    date = models.DateField()
    title = models.CharField(max_length=200)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_programs')
    members_present = models.PositiveIntegerField(default=0)
    total_members = models.PositiveIntegerField(default=0)
    activity_summary = models.TextField()
    achievements = models.TextField(blank=True)
    prayer_items = models.TextField(blank=True)
    upcoming_plans = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_programs')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
    def attendance_percentage(self):
        if self.total_members > 0:
            return round((self.members_present/self.total_members)*100)
        return 0
