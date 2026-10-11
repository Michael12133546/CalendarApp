from django.core.exceptions import ValidationError
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
    WEEKDAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday")


    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    weekdays = models.CharField(max_length=20, blank=True) 
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default="#dbeafe")

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.title} ({self.date})"

    def clean(self):
        if self.end_date and self.end_date < self.date:
            raise ValidationError("End date cannot be before the start date.")
        if self.weekdays and not self.end_date:
            raise ValidationError("Pick an end dateto repeat on selected weekdays.")

    def occurs_on(self, day):
        last = self.end_date or self.date
        if day < self.date or day > last:
            return False
        if not self.weekdays:
            return True
        return day.weekday() in [int(x) for x in self.weekdays.split(",")]