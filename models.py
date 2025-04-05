from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils.timezone import now

class DetectionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='uploads/')  # Stored in 'media/uploads/'
    result = models.CharField(max_length=255)
    # timestamp = models.DateTimeField(auto_now_add=True)
    detected_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the detection occurred
    # image = models.ImageField(upload_to='uploads/')
    # result = models.TextField()
    timestamp = models.DateTimeField(default=now)
    # image = models.ImageField(upload_to='uploads/')  # Stores uploaded images
    # result = models.CharField(max_length=100, blank=True, null=True)  # Detection result (e.g., "Pothole Detected")
    confidence = models.FloatField(blank=True, null=True)  # Confidence score (optional)
    # timestamp = models.DateTimeField(auto_now_add=True)  # Automatically adds the current time



    def __str__(self):
         return f"{self.result} - {self.confidence}"
        #  return f"Detection: {self.result} at {self.detected_at}"
        # return f"Detection on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

