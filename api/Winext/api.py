from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import User, Role

class UserIndexAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})
    
class RoleIndexAPIView(APIView):
    def get(self, request):
        role = Role.objects.all()
        serializer = RoleSerializer(role, many=True)
        return Response({"Role": serializer.data})
    
# ya tengo index en posmant, necesito crear los post (envios de info), show (mostrar por id = pk, es un get), update (actualizar datos), delete (borrar), restore (recuperar), de cada una de las apis
# ademas, hacer el login register, y log out, 
# hacer validacaion con try y except en el back (api.py)
