import logging
from django.core.mail import send_mail
from django.template import loader
from magic_links.models import MagicLinkCredential
from magic_links.settings import api_settings
from magic_links.utils import get_magic_link, inject_template_context


logger = logging.getLogger(__name__)


def send_magic_link(
        user, 
        source, 
        email_subject=api_settings.MAGIC_LINKS_EMAIL_SUBJECT,
        email_plaintext=api_settings.MAGIC_LINKS_EMAIL_PLAINTEXT_MESSAGE,
        email_html=api_settings.MAGIC_LINKS_EMAIL_HTML_TEMPLATE_NAME,
        **kwargs
    ):

    link = get_magic_link(user=user, source=source)

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
                logger.debug("No MAGIC_LINKS_EMAIL_FROM_ADDRESS specified.")
                return False
            return True

        except Exception as e:
            logger.debug(e)
            return False

        return success

    return logger.debug("Could not generate link.")

