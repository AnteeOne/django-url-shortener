import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from url_shortener.models import Url


class ShortenerForm(forms.ModelForm):
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "Paste your long URL"}))

    def clean_long_url(self):
        url = self.cleaned_data['long_url']
        pattern = 'https?:\/\/*'
        validation_error_message = "Enter a URL"
        if not re.match(pattern, url):
            raise ValidationError(validation_error_message)
        return url

    class Meta:
        model = Url
        exclude = ["user"]
        fields = ('long_url',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password 2', widget=forms.PasswordInput)

    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
