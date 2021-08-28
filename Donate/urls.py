from django.urls import path
from . import views

urlpatterns = [
    path('make/', views.create_donate_view),
    path('modify/', views.change_donate_view)
]