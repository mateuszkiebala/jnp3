from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.training, name='training'),
    url(r'^update_training/', views.update_training, name='update_training'),
]
