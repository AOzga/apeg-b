from authlib.integrations.django_oauth2 import ResourceProtector
from django.http import JsonResponse
from . import vldtr

require_auth = ResourceProtector()
validator = vldtr.Auth0JWTBearerTokenValidator(
    "dev-7namrc25ifklukgc.uk.auth0.com",
    "http://localhost:8000/"
)
require_auth.register_token_validator(validator)


def public(request):
    response = "rolled1"
    return JsonResponse(dict(message=response))


@require_auth(None)
def private(request):
    response = "rolled10"
    return JsonResponse(dict(message=response))


@require_auth("be:admin")
def private_scoped(request):
    response = "rolled20"
    return JsonResponse(dict(message=response))