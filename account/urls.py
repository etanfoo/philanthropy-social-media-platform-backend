from django.urls import path
from account.views import(
    registration_view,
    LoginView,
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'

urlpatterns = [
    path('register', registration_view),
    path('login', LoginView.as_view()), 
]