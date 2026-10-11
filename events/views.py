import calendar
from datetime import date

import holidays
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import EventForm
from .models import Event

from django.db.models import Q



# Create your views here.
def calendar_view(request, year=None, month=None):
    today = date.today()
    year = year or today.year
    month = month or today.month

    cal = calendar.Calendar(firstweekday=6)
    month_weeks = cal.monthdatescalendar(year, month)

    us_holidays = holidays.US(years=[year - 1, year, year + 1])

    first_day, last_day = month_weeks[0][0], month_weeks[-1][-1]
    events = Event.objects.filter(date__lte=last_day).filter(
        Q(end_date__gte=first_day) | Q(end_date__isnull=True, date__gte=first_day)
    )
    
    weeks = [
        [
            {
                "date": d,
                "in_month": d.month == month,
                "is_today": d == today,
                "holiday": us_holidays.get(d),
                "events": [e for e in events if e.occurs_on(d)],
            }
            for d in week
        ]
        for week in month_weeks
    ]
    prev_year, prev_month = (year - 1, 12) if month == 1 else (year, month -1)
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)

    context = {
        "weeks": weeks,
        "month_name": calendar.month_name[month],
        "year": year,
        "prev_year": prev_year, "prev_month": prev_month,
        "next_year": next_year, "next_month": next_month,
        "weekdays": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    }
    return render(request, "events/calendar.html", context)


def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect("calendar_month", year=event.date.year, month=event.date.month)
    else:
        form = EventForm(initial={"date": request.GET.get("date")})
    return render(request, "events/add_event.html", {"form": form})


@require_POST
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    year, month = event.date.year, event.date.month
    event.delete()
    return redirect("calendar_month", year=year, month=month)