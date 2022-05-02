from django.urls import path

from url_shortener.views import home_view, redirect_url_view, sign_in_view, sign_up_view, sign_out_view, urls_view

appname = "url_shortener"

urlpatterns = [
    path("", home_view, name="home"),
    path("urls", urls_view, name="urls"),
    path('signin', sign_in_view, name='signin'),
    path('signup', sign_up_view, name="signup"),
    path('signout', sign_out_view, name="signout"),
    path('<str:shortened_part>', redirect_url_view, name='redirect')
]
