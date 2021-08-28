from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post_view),
    path('all/', views.PostListView.as_view())
]