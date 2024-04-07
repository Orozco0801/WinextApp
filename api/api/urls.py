from django.urls import path
from Winext.api import UserIndexAPIView

urlpatterns = [
    path('users', UserIndexAPIView.as_view(), name='user-list'),
]
