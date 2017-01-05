from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.training, name='training'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^non_feedback/$', views.nonFeedback, name='non_feedback'),
    url(r'^time_limited/(?P<feedbackType>\w{0,50})/$', views.timeLimited, name='time_limited'),
    url(r'^timeless/(?P<feedbackType>\w{0,50})/$', views.timeless, name='timeless'),
    url(r'^game/$', views.game, name='game'),
]