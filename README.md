# CalendarApp

A calendar web app built with Python and Django for the CSCE 490/492
Research Milestone.

## Features
- Month view with navigation, today highlighted, and US holidays shown
- Add events with a title, description, date, optional end date, and times
- Multi-day events that span several days
- Events that repeat on selected weekdays (e.g. Mon/Wed) between two dates
- Choose an event color from a preset list
- Delete events from the calendar

## Tech stack
- Python and Django
- `uv` for package management
- SQLite locally, PostgreSQL (Neon) in production via `DATABASE_URL`
- Deployed on Render with gunicorn and WhiteNoise
- `holidays` library for holiday data

## Run it locally
```
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```
Then open http://127.0.0.1:8000/

## Author
Michael (GitHub: Michael12133546)
