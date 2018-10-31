import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MagicLinkCredentialManger(models.Manager):
    
    def active(self):
        return self.get_queryset().filter(is_active=True)

    def inactive(self):
        return self.get_queryset().filter(is_active=False)


class MagicLinkCredential(models.Model):

    key         = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=None, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)
    
    objects     = MagicLinkCredentialManger()

    class Meta:
        get_latest_by = 'created_at'
        ordering = ('-created_at',)
        unique_together = (('key', 'user', 'is_active'),)
        verbose_name = _('Magic Link Credentials')

    def __str__(self):
        return str(self.key)
