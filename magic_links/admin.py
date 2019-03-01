from django.contrib import admin
from .models import MagicLinkCredential


class MagicLinkCredentialAdmin(admin.ModelAdmin):
    list_display = ('key', 'created_at', 'user', 'is_active',) 

admin.site.register(MagicLinkCredential, MagicLinkCredentialAdmin)
