from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

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


class RoleListCreateAPIView(APIView):
    # Muestra todos los roles y permite crear un nuevo rol
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleRetrieveUpdateDestroyAPIView(APIView):
    # Obtiene un objeto de rol específico, maneja los casos donde no se encuentra el rol
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            raise Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

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
    # Método para reactivar un rol eliminado
    def get_object(self, pk):
        try:
            return Role.objects.only_deleted().get(pk=pk)
        except Role.DoesNotExist:
            raise Response({"error": "Rol no existe"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        role = self.get_object(pk)
        role.restore()
        return Response(status=status.HTTP_200_OK)

# ya tengo index en posmant, necesito crear los post (envios de info), show (mostrar por id = pk, es un get), update (actualizar datos), delete (borrar), restore (recuperar), de cada una de las apis
# ademas, hacer el login register, y log out, 
# hacer validacaion con try y except en el back (api.py)
