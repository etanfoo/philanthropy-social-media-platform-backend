from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post_view),
    path('all/', views.PostListView.as_view()),
    path('get/', views.get_post_view),
    path('change/', views.change_post_view),
    path('share/', views.create_shared_post_view),
    path('feed/', views.get_feed_view),
    path('userposts/', views.ProfilePostsView.as_view()),
]