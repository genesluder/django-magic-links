from django.shortcuts import redirect


def auth_redirect(request):
	source = request.GET.get('source')
	url = get_redirect_url(source, request.GET)
    return redirect('url)