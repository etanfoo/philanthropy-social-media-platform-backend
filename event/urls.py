from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_event_view),
    path('change/', views.change_event_view),
    path('all/', views.EventListView.as_view()),
    path('userevents/', views.ProfileEventsView.as_view()),
    path('get/', views.get_event_view),
    path('isattending/', views.is_attending_event),
    path('eventsattending/', views.get_user_attending_events_view)
]