from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User

class UserIndexAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})