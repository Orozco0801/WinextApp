from django.shortcuts import render

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


