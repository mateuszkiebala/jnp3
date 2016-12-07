from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.interface, name='interface'),
]