from rest_framework.views import APIView
from rest_framework.response import Response

from account.serializer import LoginSerializer


class UserLogin(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    

