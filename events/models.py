from django.db import models

# Create your models here.
class Event(models.Model):
    COLOR_CHOICES = [
        ("#fecaca", "Red"),
        ("#fed7aa", "Orange"),
        ("#fef08a", "Yellow"),
        ("#bbf7d0", "Green"),
        ("#dbeafe", "Blue"),
        ("#e9d5ff", "Purple"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default="dbeafe")

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.title} ({self.date})"
