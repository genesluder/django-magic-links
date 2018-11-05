from django.conf.urls import url
from magic_links.views.api import (
     RequestMagicLink,
     AuthTokenFromMagicLinkToken,
)


urlpatterns = [
     url('auth/email/', RequestMagicLink.as_view(), name='auth_email'),
     url('auth/token/', AuthTokenFromMagicLinkToken.as_view(), name='auth_token'),
]
