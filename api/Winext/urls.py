from django.urls import path
from .api import *

urlpatterns = [
    # listar y crear usuarios
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    # recuperar, actualizar o eliminar un usuario específico
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
    # restaurar un usuario específico
    path('users/<int:pk>/restore/', UserRestoreAPIView.as_view(), name='user-restore'),
]
