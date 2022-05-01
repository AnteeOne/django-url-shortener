from django.urls import path

from url_shortener.views import home_view, redirect_url_view

appname = "shortener"

urlpatterns = [
    path("", home_view, name="home"),
    path('<str:shortened_part>', redirect_url_view, name='redirect')
]
