# Create a new file: authentication.py
from typing import Optional, Tuple
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[object, Token]]:
        header = self.get_header(request)
        print("HTTP_AUTHORIZATION:", request.META.get('HTTP_AUTHORIZATION')) # Debug print

        if header is None:
            # Look for the token in cookies if header is missing
            raw_token = request.COOKIES.get('access_token')
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
    
    