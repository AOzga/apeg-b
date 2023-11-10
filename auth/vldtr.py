import json
from urllib.request import urlopen
from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
from authlib.jose import jwt, JoseError, JWTClaims
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience):
        issuer = f"https://{domain}/"
        jsonurl = urlopen(f"{issuer}.well-known/jwks.json")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        super(Auth0JWTBearerTokenValidator, self).__init__(
            public_key
        )
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": issuer},
        }

    def authenticate_token(self, token_string):
        try:
            claims = jwt.decode(
                token_string, self.public_key,
                claims_options=self.claims_options,
                claims_cls=self.token_cls,
            )
            claims.validate()

            return claims
        except JoseError as error:
            return None



class DRFCA(authentication.BaseAuthentication):
    def authenticate(self, request):
        validator = Auth0JWTBearerTokenValidator(
            "dev-7namrc25ifklukgc.uk.auth0.com",
            "http://localhost:8000/"
        )

        auth = request.META.get("HTTP_AUTHORIZATION", None)
        parts = auth.split()
        token = parts[1]

        try:
            clms = validator.authenticate_token(token)
            if z:=clms.get('sub'):
                a,b = User.objects.get_or_create(username=z.split('|')[1],password='')
                return a,token
        except JoseError as er:
            return None
        return None


