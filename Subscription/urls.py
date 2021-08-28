from django.urls import path

from Subscription.views import(
    subscribe_view,
    unsubscribe_view
)

app_name = 'Subscription'

urlpatterns = [
    path('subscribe', subscribe_view),
    path('unsubscribe', unsubscribe_view)
]