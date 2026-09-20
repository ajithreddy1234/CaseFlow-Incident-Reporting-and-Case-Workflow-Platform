from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
    
class UserCrimeReport(models.Model):
    CRIME_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Investigation', 'Under Investigation'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]

    PRIORITY_CHOICES = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
        (5, 'Critical'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    typeofCrime = models.CharField(max_length=100, verbose_name="Type of Crime")
    description = models.TextField(verbose_name="Crime Description", default="No description provided.")  
    location = models.CharField(max_length=255, default="Unknown Location", verbose_name="Crime Location")
    latitude = models.CharField(max_length=255, default="0", verbose_name="Latitude")
    longitude = models.CharField(max_length=255, default="0", verbose_name="Longitude")
    date = models.DateTimeField(default=timezone.now, verbose_name="Reported Date")
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name="Submitted At")
    status = models.CharField(max_length=20, choices=CRIME_STATUS_CHOICES, default='Pending', verbose_name="Report Status")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name="Priority Level")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Admin Notes")

    def __str__(self):
        return f"Report {self.id} - {self.typeofCrime} - {self.status}"
 
class Alerts(models.Model):
    
    SEVERITY_CHOICES = [
    ('info', 'Information'),
    ('warning', 'Warning'),
    ('critical', 'Critical'),
    ]


    title = models.CharField(max_length=100, verbose_name="Type of Alert")
    message = models.TextField(verbose_name="Alert Description", default="No description provided.")  
    area = models.CharField(max_length=255, default="Unknown Location", verbose_name="area")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    severity = models.CharField(choices=SEVERITY_CHOICES, max_length=10, default='info')

    def __str__(self):
        return f"Alert {self.id} - {self.title} - {self.area}"

class EvidencePhoto(models.Model):
    report = models.ForeignKey(UserCrimeReport, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='evidence_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for Report {self.report.id}"
    
class EvidenceVideo(models.Model):
    report = models.ForeignKey(UserCrimeReport, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='evidence_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for Report {self.report.id}"


class EvidenceAudio(models.Model):
    report = models.ForeignKey(UserCrimeReport, on_delete=models.CASCADE, related_name='audios')
    audio = models.FileField(upload_to='evidence_audios/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio for Report {self.report.id}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Title of Notification")
    message = models.TextField(verbose_name="Notification Message", default="Context not provided")
    date = models.DateTimeField(default=timezone.now, verbose_name="Notification Date")
    is_read = models.BooleanField(default=False, verbose_name="Read Status")
    
    related_report = models.ForeignKey(UserCrimeReport, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    related_alert = models.ForeignKey(Alerts, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')

    def __str__(self):
        return f"Notification to {self.user.username} - {self.title}"
