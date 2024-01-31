from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ExpiringTokenAuthentication(TokenAuthentication):
    
    def expires_in(self,token):
        # devuelve el tiempo que le queda al token
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self,token):
        # devuelve True si el token persiste o False si expiro
        return self.expires_in(token) < timedelta(seconds = 0)

    def token_expire_handler(self,token):
        """
        Return:
            * is_expire     : Devuelve True si el token persiste o False si expiro
            * token         : Token nuevo o Token actual
        """
        is_expire = self.is_token_expired(token)
        if is_expire:
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user=user)
        
        return token

    def authenticate_credentials(self,key):
        """
        Return:
            * user      : Instancia de User que envio la request
            * token     : Token nuevo o Token actual para el user
            * message   : Mensaje de error
            * expired   : Devuelve True si el token persiste o False si expiro
        """
        user = None
        try:
            token = self.get_model().objects.select_related('user').get(key=key)
            token = self.token_expire_handler(token)
            user = token.user
        except self.get_model().DoesNotExist:
            pass

        return user
