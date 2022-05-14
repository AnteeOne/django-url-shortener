from django.contrib.auth import get_user_model
from django.test import TestCase

from app import settings
from url_shortener.forms import ShortenerForm
from url_shortener.models import Url
from url_shortener.utils import create_random_code


class AuthTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        username = 'test_user'
        password = "test_user_pass"
        user = User.objects.create_user(username=username, password=password)

    def test_sign_in_success(self):
        username = 'test_user'
        password = "test_user_pass"
        self.client.login(username=username, password=password)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_sign_in_fail(self):
        username = 'test_user'
        password = "test_user_pass_with_error"
        self.client.login(username=username, password=password)
        response = self.client.get('/urls')
        self.assertEqual(response.status_code, 302)


class ViewsTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        username = 'test_user'
        password = "test_user_pass"
        user = User.objects.create_user(username=username, password=password)

    def test_signin_loads_properly(self):
        response = self.client.get('/signin')
        self.assertEqual(response.status_code, 200)

    def test_signup_loads_properly(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_signout_loads_properly(self):
        response = self.client.get('/signout')
        self.assertEqual(response.status_code, 302)

    def test_urls_loads_properly(self):
        response = self.client.get('/urls')
        self.assertEqual(response.status_code, 302)

    def test_sign_in_uses_correct_template(self):
        response = self.client.get('/signin')
        self.assertTemplateUsed(response, 'url_shortener/sign_in.html')

    def test_sign_up_uses_correct_template(self):
        response = self.client.get('/signup')
        self.assertTemplateUsed(response, 'url_shortener/sign_up.html')

    def test_home_uses_correct_template(self):
        username = 'test_user'
        password = "test_user_pass"
        self.client.login(username=username, password=password)
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'url_shortener/home.html')

    def test_urls_uses_correct_template(self):
        username = 'test_user'
        password = "test_user_pass"
        self.client.login(username=username, password=password)
        response = self.client.get('/urls')
        self.assertTemplateUsed(response, 'url_shortener/urls.html')

    def test_home_post_uses_correct_template(self):
        username = 'test_user'
        password = "test_user_pass"
        self.client.login(username=username, password=password)
        form_data = {'long_url': 'https://www.google.com/'}
        response = self.client.post('/', form_data)
        self.assertTemplateUsed(response, 'url_shortener/home.html')


class UrlFormTestCase(TestCase):

    def test_url_form_is_valid(self):
        form_data = {'long_url': 'https://www.google.com/'}
        url_form = ShortenerForm(form_data)
        self.assertTrue(url_form.is_valid())

    def test_url_form_is_invalid(self):
        form_data = {'long_url': 'some_fake_url'}
        url_form = ShortenerForm(form_data)
        print(url_form.data.get('long_url'))
        self.assertFalse(url_form.is_valid())


class ShortUrlTestCase(TestCase):

    def test_random_code_size(self):
        self.assertTrue(len(create_random_code()) == getattr(settings, "MAXIMUM_URL_CHARS"))

    def test_create_unique_random_url_works_correctly(self):
        User = get_user_model()
        username = 'test_user'
        password = "test_user_pass"
        user = User.objects.create_user(username=username, password=password)

        long_url = 'https://www.google.com/'
        urls_count = 10000
        for i in range(urls_count):
            Url.objects.create(long_url=long_url, user=user)
        self.assertTrue(Url.objects.count() == urls_count)

    def test_redirect_works_correctly(self):
        User = get_user_model()
        username = 'test_user'
        password = "test_user_pass"
        user = User.objects.create_user(username=username, password=password)

        long_url = 'https://www.google.com/'
        Url.objects.create(long_url=long_url, user=user)
        response = self.client.get('/' + Url.objects.get(id=1).short_url)
        self.assertURLEqual(response.url, long_url)
