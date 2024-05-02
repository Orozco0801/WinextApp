from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from core.models import *
from django.http import Http404
from .permissions import *
from django.utils import timezone
from django.db.utils import IntegrityError

# ------------------------------------------------------------------------------------------------------------
# User
# ------------------------------------------------------------------------------------------------------------
# Listar y crear usuarios no eliminados
class UserListCreateAPIView(APIView):
    def get(self, request):
        try:
            # Mostrar todos los usuarios no eliminados.
            users = User.objects.filter(is_deleted=False)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            # Crear usuario, validar y guardar.
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Recuperar, actualizar o eliminar (soft delete)
class UserRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            # Obtener usuario por ID no eliminado.
            return User.objects.get(pk=pk, is_deleted=False)
        except User.DoesNotExist:
            raise Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            # Obtener y devolver los datos
            user = self.get_object(pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            # Actualizar un usuario específico
            user = self.get_object(pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            # Marcar un usuario como eliminado
            user = self.get_object(pk)
            user.is_deleted = True
            user.deleted_at = timezone.now()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Restaurar un usuario
class UserRestoreAPIView(APIView):
    def get_object(self, pk):
        try:
            # Obtener usuario por ID eliminado
            return User.objects.get(pk=pk, is_deleted=True)
        except User.DoesNotExist:
            raise Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            # Restaurar un usuario marcado como eliminado.
            user = self.get_object(pk)
            user.is_deleted = False
            user.deleted_at = None
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------------------------------------------------------------
# Roles
# ------------------------------------------------------------------------------------------------------------
# Listar todos los roles y permitir la creación de nuevos roles.
class RoleListCreateAPIView(APIView):
    def get(self, request):
        try:
            roles = Role.objects.filter(is_deleted=False)
            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data)
        except Role.DoesNotExist:
            raise Response({"error": "Roles not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RoleRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk, is_deleted=False)
        except Role.DoesNotExist:
            raise Http404("Role not found")

    def get(self, request, pk):
        try:
            role = self.get_object(pk)
            serializer = RoleSerializer(role)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            role = self.get_object(pk)
            serializer = RoleSerializer(role, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            role = self.get_object(pk)
            role.deleted_at = timezone.now()
            role.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RoleRestoreAPIView(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk, is_deleted=True)
        except Role.DoesNotExist:
            raise Http404("Role not found")

    def put(self, request, pk):
        try:
            role = self.get_object(pk)
            role.deleted_at = None
            role.restore()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------------------------------------------------------------
# Vehicle mostrar y actualizar solamente
# ------------------------------------------------------------------------------------------------------------
class VehicleRetrieveUpdateAPIView(APIView):
    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk, is_deleted=False)
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            vehicle = self.get_object(pk)
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            vehicle = self.get_object(pk)
            serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------------------------------------------------------------
# Profile
# ------------------------------------------------------------------------------------------------------------
class ProfileListAPIView(APIView):
    def get(self, request):
        try:
            profiles = Profile.objects.filter(is_deleted=False)
            serializer = ProfileSerializer(profiles, many=True)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            raise Response({"error": "Profiles not found"}, status=status.HTTP_404_NOT_FOUND)

class ProfileDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk, is_deleted=False)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            profile = self.get_object(pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            profile = self.get_object(pk)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            profile = self.get_object(pk)
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------------------
# Trip
# ------------------------------------------------------------------------------------------------------------
# Crear y listar viajes para clientes
class TripListCreateAPIView(APIView):
    permission_classes = [IsClient]  # Permite solo a clientes

    def get(self, request):
        try:
            trips = Trip.objects.filter(client=request.user, is_deleted=False)
            serializer = TripSerializer(trips, many=True)
            return Response(serializer.data)
        except Trip.DoesNotExist:
            raise Response({"error": "Trips not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            serializer = TripSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(client=request.user)  # Asegúrate de que el cliente sea el usuario autenticado
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Detalles del viaje, aceptación y actualización por parte del taxista
class TripRetrieveUpdateAPIView(APIView):
    permission_classes = [IsDriver]  # Permite solo a taxistas

    def get_object(self, pk):
        try:
            trip = Trip.objects.get(pk=pk, is_deleted=False)
            if trip.driver is None or trip.driver == self.request.user:
                return trip
            else:
                raise Http404("This trip has already been accepted by another driver.")
        except Trip.DoesNotExist:
            raise Http404("Trip not found")

    def get(self, request, pk):
        try:
            trip = self.get_object(pk)
            serializer = TripSerializer(trip)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            trip = self.get_object(pk)
            serializer = TripSerializer(trip, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save(driver=request.user) 
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            trip = self.get_object(pk)
            trip.is_deleted = True
            trip.deleted_at = timezone.now()
            trip.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Restaurar un viaje
class TripRestoreAPIView(APIView):
    def get_object(self, pk):
        try:
            # Obtener viaje por ID eliminado
            return Trip.objects.get(pk=pk, is_deleted=True)
        except Trip.DoesNotExist:
            raise Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            # Restaurar un viaje marcado como eliminado.
            trip = self.get_object(pk)
            trip.is_deleted = False
            trip.deleted_at = None
            trip.save()
            serializer = TripSerializer(trip)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)