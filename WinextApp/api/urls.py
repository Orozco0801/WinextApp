from django.urls import path
from .api import *

urlpatterns = [
    # Usuarios
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
    path('users/<int:pk>/restore/', UserRestoreAPIView.as_view(), name='user-restore'),

    # Roles
    path('roles/', RoleListCreateAPIView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroyAPIView.as_view(), name='role-retrieve-update-destroy'),
    path('roles/<int:pk>/restore/', RoleRestoreAPIView.as_view(), name='role-restore'),

    # Viajes
    path('trips/', TripListCreateAPIView.as_view(), name='trip-list-create'),
    path('trips/<int:pk>/', TripRetrieveUpdateAPIView.as_view(), name='trip-retrieve-update'),
    path('trips/<int:pk>/restore/', TripRestoreAPIView.as_view(), name='trip-restore'),

    # Vehículos
    path('vehicles/<int:pk>/', VehicleRetrieveUpdateAPIView.as_view(), name='vehicle-retrieve-update'),

    # Perfiles
    path('profiles/', ProfileListAPIView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetailAPIView.as_view(), name='profile-detail'),
]
