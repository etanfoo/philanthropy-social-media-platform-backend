from django.urls import path
from . import views

urlpatterns = [
    path('make/', views.create_donate_view),
    path('modify/', views.change_donate_view),
    path('remove/', views.delete_donate_view),
    path('userdonates/', views.ProfileDonatesView.as_view())
]