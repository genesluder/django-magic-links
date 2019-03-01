from django.urls import path
from magic_links.views.api import (
     RequestMagicLink,
     AuthenticateToken,
)


urlpatterns = [
     path('auth/email/', RequestMagicLink.as_view(), name='magic_link_email'),
     path('auth/token/', AuthenticateToken.as_view(), name='magic_link_token'),
]
