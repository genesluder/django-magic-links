import logging
from django.core.mail import send_mail
from django.template import loader
from magic_links.exceptions import (
    InvalidKeyException,
    MagicLinkException,
    TokenAllocationException,
    UserInactiveException,
    UserNotFoundException,
)
from magic_links.models import MagicLinkCredential
from magic_links.settings import api_settings
from magic_links.utils import (
    authenticate_user,
    check_credential_expiry,
    check_hashed_key,
    get_magic_link,
    get_user_for_email,
    inject_template_context,
)


logger = logging.getLogger(__name__)


def email_link(
        user, 
        request_source, 
        go_next=None,
        email_subject=api_settings.MAGIC_LINKS_EMAIL_SUBJECT,
        email_plaintext=api_settings.MAGIC_LINKS_EMAIL_PLAINTEXT_MESSAGE,
        email_html=api_settings.MAGIC_LINKS_EMAIL_HTML_TEMPLATE_NAME,
        **kwargs
    ):

    link = get_magic_link(user=user, request_source=request_source, go_next=go_next)

    if link:

        try:
            if api_settings.MAGIC_LINKS_EMAIL_FROM_ADDRESS:

                context = inject_template_context({'link': link})
                html_message = loader.render_to_string(email_html, context,)
                send_mail(
                    email_subject,
                    email_plaintext.format(link=link),
                    api_settings.MAGIC_LINKS_EMAIL_FROM_ADDRESS,
                    [ getattr(user, api_settings.MAGIC_LINKS_USER_EMAIL_FIELD_NAME) ],
                    fail_silently=False,
                    html_message=html_message,
                )

            else:
                logger.debug("Nothing specified for MAGIC_LINKS_EMAIL_FROM_ADDRESS.")
                return False
            return True

        except Exception as e:
            logger.debug(e)
            return False

        return success

    return logger.debug("Could not generate link.")


def send_magic_link(email, request_source='default', go_next=None):

    user = get_user_for_email(email)

    if not user:
        raise UserNotFoundException

    if not user.is_active:
        raise UserInactiveException

    success = email_link(user, request_source, go_next=go_next)

    if not success:
        raise MagicLinkException

    return True


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


def get_user_from_callback_token(email, callback_token):

    credential = validate_credential(email, callback_token)

    if not credential:
        raise InvalidKeyException

    user = credential.user

    if not user.is_active:
        raise UserInactiveException

    return user


def authenticate_session(email, callback_token):

    return get_user_from_callback_token(email, callback_token)


def authenticate_token(email, callback_token):

    user = get_user_from_callback_token(email, callback_token)
    token = authenticate_user(user)

    if not token:
        raise TokenAllocationException

    return token
