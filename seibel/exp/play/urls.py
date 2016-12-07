from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.play, name='play'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^non_feedback/$', views.nonFeedback, name='non_feedback'),
    url(r'^game/$', views.game, name='game'),
]