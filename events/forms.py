from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    weekdays = forms.MultipleChoiceField(
        choices=Event.WEEKDAY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Repeat on (optional)",
    )

    class Meta:
        model = Event
        fields = ["title", "description", "date", "end_date", "weekdays","start_time", "end_time", "color"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }
    def clean_weekdays(self):
        return ",".join(sorted(self.cleaned_data["weekdays"], key=int))