from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from magic_links.forms import MagicLinkForm
from magic_links.constants import MESSAGE_UNKNOWN_ERROR
from magic_links.services import (
    authenticate_session,
    send_magic_link,
)


class MagicLinkFormView(FormView):

    template_name = 'magic_link_form.html'
    form_class = MagicLinkForm

    def form_valid(self, form):
        send_magic_link(form.cleaned_data['email'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('magic_link_sent')


class AuthenticateView(TemplateView):
    
    template_name = 'error.html'

    def get(self, request):
        email = request.GET.get('email')
        callback_token = request.GET.get('token')
        source = request.GET.get('source', 'default')

        if email and callback_token:
            user = None

            try:
                user = authenticate_session(
                    email=email, 
                    callback_token=callback_token
                )
            except Exception as e:
                messages.error(request, str(e))

            if user:
                django_login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

        else:
            messages.error(request, MESSAGE_UNKNOWN_ERROR)

        return super().get(request)


def auth_redirect(request):
    source = request.GET.get('source')
    url = get_redirect_url(source, request.GET)
    return redirect('url')
