from django.urls import path
from .api import *

urlpatterns = [
    # User
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
    path('users/<int:pk>/restore/', UserRestoreAPIView.as_view(), name='user-restore'),

    # Role
    
]
