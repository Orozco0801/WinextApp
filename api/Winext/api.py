from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django_softdelete.models import SoftDeletionModel
from rest_framework.views import APIView
from .serializers import *
from .models import User, Role

class UserIndexAPIView(APIView, SoftDeletionModel):
    # Muestra todos los datos del model user, y lanza error si no lo encuentra
    def get(self, request):
        try:
            users = User.objects.all() 
            if not users:
                return Response({"error": "No se encontraron usuarios"}, status=404)
            serializer = UserSerializer(users, many=True)
            return Response({"users": serializer.data})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    #Recibe los datos, los valida y los guarda
    def post(self, request):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Busca a un usuario por su id
    def show(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Busca user por PK, los actualiza y los guarda
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Implementa soft delete o borrado suave
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Reactiva al usuario eliminado
    def restore(self, request, pk):
        try:
            user = User.objects.only_deleted().get(pk=pk)
            user.restore()
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class RoleIndexAPIView(APIView):
    def get(self, request):
        role = Role.objects.all()
        serializer = RoleSerializer(role, many=True)
        return Response({"Role": serializer.data})
    
# ya tengo index en posmant, necesito crear los post (envios de info), show (mostrar por id = pk, es un get), update (actualizar datos), delete (borrar), restore (recuperar), de cada una de las apis
# ademas, hacer el login register, y log out, 
# hacer validacaion con try y except en el back (api.py)
