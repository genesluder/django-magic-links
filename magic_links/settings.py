from django.conf import settings
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, 'MAGIC_LINKS', None)

DEFAULTS = {
    # URLS for creating links, dict key corresponds to `source` when requesting link
    'MAGIC_LINKS_URLS': {
        'default': 'http://localhost:8000/auth/'
    },

    # Amount of time that tokens last, in seconds
    'MAGIC_LINKS_EXPIRE_TIME': 15 * 60,

    # Registers previously unseen aliases as new users.
    'MAGIC_LINKS_CREATE_USER': True,

    # The user's email field name
    'MAGIC_LINKS_USER_EMAIL_FIELD_NAME': 'email',

    # The email the callback token is sent from
    'MAGIC_LINKS_EMAIL_FROM_ADDRESS': 'from@example.com',

    # The email subject
    'MAGIC_LINKS_EMAIL_SUBJECT': "Your Magic Link",

    # A plaintext email message overridden by the html message. Takes one string.
    'MAGIC_LINKS_EMAIL_PLAINTEXT_MESSAGE': "Follow this link to sign in: {link}",

    # The email template name.
    'MAGIC_LINKS_EMAIL_HTML_TEMPLATE_NAME': 'magic_link_email.html',

    # Context Processors for Email Template
    'MAGIC_LINKS_CONTEXT_PROCESSORS': [],


    # Context Processors for Email Template
    'MAGIC_LINKS_LOGIN_REDIRECT': settings.LOGIN_REDIRECT_URL,

}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'MAGIC_LINKS_EMAIL_TOKEN_HTML_TEMPLATE',
    'MAGIC_LINKS_CONTEXT_PROCESSORS',
)

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
