import bcrypt
from urllib.parse import urlencode, urlparse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from magic_links.models import MagicLinkCredential
from magic_links.settings import api_settings

User = get_user_model()


def authenticate_user(user):
    token, created = Token.objects.get_or_create(user=user)
    return token


def check_credential_expiry(credential):
    seconds = (timezone.now() - credential.created_at).total_seconds()
    credential_expiry_time = api_settings.MAGIC_LINKS_EXPIRE_TIME

    if seconds <= credential_expiry_time:
        return True

    credential.is_active = False
    credential.save()
    return False


def get_url_for_source(request_source):
    return api_settings.MAGIC_LINKS_URLS.get(request_source)


def get_redirect_url(request_source, query_params):
    base_url = get_url_for_source(request_source)
    url = '{}?{}'.format(base_url, urlencode(query_params))
    return url


def get_magic_link(user, request_source):

    # check for existing key
    credential, created = MagicLinkCredential.objects.get_or_create(user=user, is_active=True)

    if not created:
        if not check_credential_expiry(credential):
            credential = MagicLinkCredential.objects.create(user=user)

    token = get_hashed_key(str(credential.key))

    payload = {
        'email': credential.user.email, 
        'token': token,
        'source': request_source
    }

    # TODO: Error if request_source not specified
    base_url = get_url_for_source(request_source)
    url = '{}?{}'.format(base_url, urlencode(payload))

    return url


def get_user_for_email(email):
    if api_settings.MAGIC_LINKS_CREATE_USER is True:
        user, created = User.objects.get_or_create(email=email)
        if created:
            # Initially set an unusable password
            user.set_unusable_password()
            user.save()
    else:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
    return user


def get_hashed_key(plain_text_key):
    return bcrypt.hashpw(plain_text_key.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_hashed_key(plain_text_key, hashed_key):
    return bcrypt.checkpw(plain_text_key.encode('utf-8'), hashed_key.encode('utf8'))


def validate_credential(email, callback_token):
    try:
        credential = MagicLinkCredential.objects.get(user__email=email, is_active=True)

        if check_credential_expiry(credential):
            valid = check_hashed_key(str(credential.key), callback_token)
            if valid:
                credential.is_active = False
                credential.save()
                return credential
            return None
        else:
            return None

    except MagicLinkCredential.DoesNotExist:
        return None


def inject_template_context(context):
    for processor in api_settings.MAGIC_LINKS_CONTEXT_PROCESSORS:
        context.update(processor())
    return context

