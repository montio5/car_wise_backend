from apps.user.models import BlacklistedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header:
                raw_token = self.get_raw_token(header)
                if raw_token and BlacklistedToken.objects.filter(token=raw_token.decode('utf-8')).exists():
                    raise InvalidToken('Token is blacklisted')
                return super().authenticate(request)
        return super().authenticate(request)
