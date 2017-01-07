from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.play, name='play'),
    url(r'^update_results/', views.update_results, name='update_results'),
    url(r'^update_session/', views.update_session, name='update_session'),
    url(r'^update_session_start/', views.update_session_start, name='update_session_start'),
    url(r'^update_session_end/', views.update_session_end, name='update_session_end')
]