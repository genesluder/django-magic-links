from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MagicLinksConfig(AppConfig):
    name = 'magic_links'
    verbose = _("Django Magic Links")

