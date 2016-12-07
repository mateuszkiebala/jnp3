from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^training/', include('exp.training.urls')),
    url(r'^play/', include('exp.play.urls')),
]
