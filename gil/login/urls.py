from django.conf.urls import url
from . import views

urlpatterns = [
    # user auth urls
    url(r'^login_experiment/$', views.login_experiment, name='login_experiment'),
    url(r'^login_pilot_mode/$', views.login_pilot_mode, name='login_pilot_mode'),
]