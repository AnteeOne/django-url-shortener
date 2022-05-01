from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render  # We will use it later

from .forms import ShortenerForm
# Model
# Custom form
from .models import Url


def home_view(request):
    template = 'url_shortener/home.html'

    context = {}

    context['form'] = ShortenerForm()

    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':

        used_form = ShortenerForm(request.POST)

        if used_form.is_valid():
            shortened_object = used_form.save()

            new_url = request.build_absolute_uri('/') + shortened_object.short_url

            long_url = shortened_object.long_url

            context['new_url'] = new_url
            context['long_url'] = long_url

            return render(request, template, context)

        context['errors'] = used_form.errors

        return render(request, template, context)


def redirect_url_view(request, shortened_part):
    try:
        short_url = Url.objects.get(short_url=shortened_part)

        short_url.redirect_count += 1

        short_url.save()

        return HttpResponseRedirect(short_url.long_url)

    except:
        raise Http404('Sorry this link is broken :(')
