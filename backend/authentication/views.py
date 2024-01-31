from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.api.serializers import (
    CustomTokenObtainPairSerializer, CustomUserSerializer
)
from .models import User
import logging


class Login(TokenObtainPairView):
    """
    View de login que extiende TokenObtainPairView.
    
    Sobreescribe el metodo post para proporcionar 
    funciones adicionales como registrar inicios de sesión exitosos.

    Attributes:
    - serializer_class: Para manejar la adquisición de tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Maneja el POST para el login del usuario.
        """
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                self.log_activity(f'Inicio de sesión exitoso: {user}')
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de Sesion Existoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
    
    def log_activity(self, message):
        """
        Log de la actividad del usuario.
        """
        logger = logging.getLogger(__name__)
        logger.info(message)

class Logout(GenericAPIView):
    """
    View de Logout que extiende GenericAPIView.

    Sobreescribe el metodo post para manejar el logout del user y 
    registrar logouts exitosos.
    """
    def post(self, request, *args, **kwargs):
        """
        Maneja el POST para el logout del usuario.
        """
        user_id = request._auth.get('user_id', 0)
        if user_id is None:
            user_id = 0
        user = User.objects.filter(id=user_id)
        if user:
            RefreshToken.for_user(user.first())
            self.log_activity(f'Cierre de sesión exitoso: {user.first()}')
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def log_activity(self, message):
        """
        Log de la actividad del usuario.
        """
        logger = logging.getLogger(__name__)
        logger.info(message)
