from django.contrib import messages
from django.contrib.auth import login as django_login
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from magic_links.forms import MagicLinkForm
from magic_links.constants import MESSAGE_UNKNOWN_ERROR
from magic_links.settings import api_settings
from magic_links.services import (
    authenticate_session,
    send_magic_link,
)


class MagicLinkFormView(FormView):

    template_name = 'magic_link_form.html'
    form_class = MagicLinkForm

    def get_initial(self):
        initial = super(MagicLinkFormView, self).get_initial()
        initial['next'] = self.request.GET.get('next')
        return initial

    def form_valid(self, form):
        send_magic_link(
            email=form.cleaned_data['email'], 
            go_next=form.cleaned_data.get('next')
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('magic_link_sent')


class AuthenticateView(TemplateView):
    
    template_name = 'error.html'

    def get(self, request):
        email = request.GET.get('email')
        callback_token = request.GET.get('token')
        source = request.GET.get('source', 'default')
        go_next = request.GET.get('next')

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
                url = go_next or api_settings.MAGIC_LINKS_LOGIN_REDIRECT
                return redirect(url)

        else:
            messages.error(request, MESSAGE_UNKNOWN_ERROR)

        return super().get(request)


def auth_redirect(request):
    source = request.GET.get('source')
    url = get_redirect_url(source, request.GET)
    return redirect('url')
