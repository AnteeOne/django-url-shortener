from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect  # We will use it later

from .forms import ShortenerForm, UserRegistrationForm, LoginForm
# Model
# Custom form
from .models import Url


@login_required()
def home_view(request):
    template = 'url_shortener/home.html'
    current_user = request.user

    context = {}

    context['form'] = ShortenerForm()

    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':

        form = ShortenerForm(request.POST)

        if form.is_valid():
            shortened_object = form.save(commit=False)
            shortened_object.user = current_user
            shortened_object.save()

            new_url = request.build_absolute_uri('/') + shortened_object.short_url

            long_url = shortened_object.long_url

            context['new_url'] = new_url
            context['long_url'] = long_url

            return render(request, template, context)

        context['errors'] = form.errors

        return render(request, template, context)


def redirect_url_view(request, shortened_part):
    try:
        short_url = Url.objects.get(short_url=shortened_part)

        short_url.redirect_count += 1

        short_url.save()

        return HttpResponseRedirect(short_url.long_url)

    except:
        raise Http404()


def sign_up_view(request):
    template = 'url_shortener/sign_up.html'
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return HttpResponseRedirect('/signin')
        else:
            return HttpResponse("Invalid data, try again")
    else:
        user_form = UserRegistrationForm()

    return render(request, template, {'form': user_form})


def sign_in_view(request):
    template = 'url_shortener/sign_in.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, template, {'form': form})


def sign_out_view(request):
    logout(request)
    return redirect("/")


@login_required()
def urls_view(request):
    if request.method == 'POST':
        url_id = request.POST.get("url_id", "")
        Url.objects.filter(id=url_id).delete()
        return redirect("/urls")

    elif request.method == 'GET':
        current_user = request.user
        urls = Url.objects.filter(user_id=current_user.id).order_by('-redirect_count')
        template = 'url_shortener/urls.html'
        return render(request, template, {'urls': urls})
