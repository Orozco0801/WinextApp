from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.http import Http404
from .permissions import IsClient, IsDriver 

#------------------------------------------------------------------------------------------------------------
# User
#------------------------------------------------------------------------------------------------------------
# listar y crear usuarios no eliminados
class UserListCreateAPIView(APIView):
    def get(self, request):
        # mostrar todos los usuarios no eliminados.
        users = User.objects.filter(is_deleted=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        # crea usuario, validar y guardar.
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# recuperar, actualizar o eliminar (soft delete)
class UserRetrieveUpdateDestroyAPIView(APIView):

    def get_object(self, pk):
        # obtener usuario por ID  no eliminado.
        try:
            return User.objects.get(pk=pk, is_deleted=False)
        except User.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        # Obtener y devolver los datos
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        # Actualizar  un usuario específico 
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # marca un usuario como eliminado
        user = self.get_object(pk)
        user.is_deleted = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

# restaurar un usuario
class UserRestoreAPIView(APIView):
    def get_object(self, pk):
        #  obtener usuario por ID eliminado
        try:
            return User.objects.get(pk=pk, is_deleted=True)
        except User.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        # Restaurar un usuario marcado como eliminado.
        user = self.get_object(pk)
        user.is_deleted = False
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


#------------------------------------------------------------------------------------------------------------
# Roles
#------------------------------------------------------------------------------------------------------------
# listar todos los roles y permitir la creación de nuevos roles.
class RoleListCreateAPIView(APIView):
    def get(self, request):
        roles = Role.objects.filter(is_deleted=False)
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk, is_deleted=False)
        except Role.DoesNotExist:
            raise Http404("Role not found")

    def get(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    def put(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoleRestoreAPIView(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk, is_deleted=True)
        except Role.DoesNotExist:
            raise Http404("Role not found")

    def put(self, request, pk):
        role = self.get_object(pk)
        role.restore()
        return Response(status=status.HTTP_200_OK)


#------------------------------------------------------------------------------------------------------------
# Vehicle mostrar y actualizar solamente
#------------------------------------------------------------------------------------------------------------
class VehicleRetrieveUpdateAPIView(APIView):
    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk, is_deleted=False)
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        vehicle = self.get_object(pk)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    def put(self, request, pk):
        vehicle = self.get_object(pk)
        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#------------------------------------------------------------------------------------------------------------
# Profile
#------------------------------------------------------------------------------------------------------------
class ProfileListAPIView(APIView):
    def get(self, request):
        profiles = Profile.objects.filter(is_deleted=False)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

class ProfileDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk, is_deleted=False)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#------------------------------------------------------------------------------------------------------------
# Trip
#------------------------------------------------------------------------------------------------------------
# Crear y listar viajes para clientes
class TripListCreateAPIView(APIView):
    permission_classes = [IsClient]  # Permite solo a clientes

    def get(self, request):
        trips = Trip.objects.filter(client=request.user, is_deleted=False)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TripSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(client=request.user)  # Asegúrate de que el cliente sea el usuario autenticado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        trip = self.get_object(pk)
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    def put(self, request, pk):
        trip = self.get_object(pk)
        serializer = TripSerializer(trip, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save(driver=request.user)  # Asegúrate de asignar el taxista al viaje
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)