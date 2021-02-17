import jwt
from django.contrib import auth
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from django.conf import settings


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer;

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):

    def post(self, request):
        data = request.data;
        email = data.get('email', '')
        password = data.get('password', '')
        user = auth.authenticate(username=email, password=password)
        temp = settings.JWT_SECRET_KEY
        if user:
            auth_token = jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY)
            serializer = UserSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        try:
            return Response(UserSerializer(request.user, context={'request': request}).data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Wrong auth token' + e}, status=status.HTTP_400_BAD_REQUEST)
