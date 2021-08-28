from django.urls import path
from . import views

urlpatterns = [
    path('make/', views.create_donate_view)
]