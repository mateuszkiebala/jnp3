from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.play, name='play'),
    url(r'^update_results/', views.update_results, name='update_results'),
    url(r'^update_session/', views.update_session, name='update_session')
]