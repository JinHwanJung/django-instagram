from django.urls import path

from notification.views import Notifications

app_name = "notification"

urlpatterns = [
    path(r'', Notifications.as_view(), name='notifications'),
]
