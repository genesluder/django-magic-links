from django.urls import path
from django.views.generic import TemplateView
from magic_links.views.www import (
    MagicLinkFormView,
    AuthenticateView,
)


urlpatterns = [
     path('login-sent/', TemplateView.as_view(template_name='magic_link_sent.html'), name='magic_link_sent'),
     path('login/', MagicLinkFormView.as_view(), name='magic_link_login'),
     path('auth/', AuthenticateView.as_view(), name='magic_link_auth'),
]
