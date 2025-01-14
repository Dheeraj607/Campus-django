from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Notification(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    type=models.IntegerField(null=True)

    def __str__(self):
        return f"Notification for Event: {self.id}"

class Request(models.Model):
    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Accepted'),
        (2, 'Rejected'),
    ]

    req_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    message = models.TextField()
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, null=True)
    replay=models.TextField(null=True,default="")

    def __str__(self):
        return f"Request from {self.req_from.username} (ID: {self.id})"
