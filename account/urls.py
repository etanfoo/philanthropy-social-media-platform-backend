from django.urls import path
from account.views import(
    registration_view,
    LoginView,
    account_profile_view,
    logout_view,
    ApiAccountListView,
    get_subscriber_view,
    get_subscribing_view,
    update_account_view,
    update_password_view
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'

urlpatterns = [
    path('register', registration_view),
    path('login', LoginView.as_view()), 
    path('profile', account_profile_view),
    path('logout', logout_view),
    path('explore', ApiAccountListView.as_view()),
    path('subscribers', get_subscriber_view),
    path('subscribing', get_subscribing_view),
    path('edit', update_account_view),
    path('changepassword', update_password_view),
]