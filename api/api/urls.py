from django.urls import path
from Winext.api import *

urlpatterns = [
    
    path('users', UserIndexAPIView.as_view(), name='user-list'),
    path('role', RoleIndexAPIView.as_view(), name='role-list'),
]
