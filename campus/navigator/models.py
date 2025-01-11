from django.db import models

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
