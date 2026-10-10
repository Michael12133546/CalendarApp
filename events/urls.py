from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name="calendar"),
    path("<int:year>/<int:month>/", views.calendar_view, name="calendar_month"),
]