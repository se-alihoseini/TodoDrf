from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import login, logout, authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterView(APIView):
    """
    This view is for user registration
    """
    serializer_class = UserRegisterSerializer

    def post(self, request):
        srz_data = UserRegisterSerializer(data=request.POST)
        if srz_data.is_valid():
            srz_data.create(srz_data.validated_data)
            return Response(srz_data.data['username'], status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    This view is for user login
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        srz_data = UserLoginSerializer(data=request.POST)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            user = authenticate(request, username=vd['username'], password=vd['password'])
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                return Response({'token': token, 'refresh': str(refresh)}, status=status.HTTP_200_OK)
            return Response('user does not exist', status=status.HTTP_401_UNAUTHORIZED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """
    This view is for user logout
    """

    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        logout(request)
        return Response('logout shodi', status=status.HTTP_200_OK)
