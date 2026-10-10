import calendar
from datetime import date

import holidays
from django.shortcuts import render

from .models import Event


# Create your views here.
def calendar_view(request, year=None, month=None):
    today = date.today()
    year = year or today.year
    month = month or today.month

    cal = calendar.Calendar(firstweekday=6)
    month_weeks = cal.monthdatescalendar(year, month)

    us_holidays = holidays.US(years=[year - 1, year, year + 1])

    first_day, last_day = month_weeks[0][0], month_weeks[-1][-1]
    events = Event.objects.filter(date__range=(first_day, last_day))
    events_by_day = {}
    for e in events:
        events_by_day.setdefault(e.date, []).append(e)

    weeks = [
        [
            {
                "date": d,
                "in_month": d.month == month,
                "is_today": d == today,
                "holiday": us_holidays.get(d),
                "events": events_by_day.get(d, []),
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
    