from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^welcome/', views.welcome, name='welcome'),
    url(r'^welcome_training_gil/', views.welcome_training_gil, name='welcome_training_gil'),
    url(r'^training_gil/', views.training_gil, name='training_gil'),
    url(r'^welcome_survey_gil/', views.welcome_survey_gil, name='welcome_survey_gil'),
    url(r'^survey_gil/', views.survey_gil, name='survey_gil'),
    url(r'^survey_gil_save_clicks/', views.survey_gil_save_clicks, name='survey_gil_save_clicks'),
    url(r'^welcome_training_selection/', views.welcome_training_selection, name='welcome_training_selection'),
    url(r'^training_selection/', views.training_selection, name='training_selection'),
    url(r'^welcome_survey_selection/', views.welcome_survey_selection, name='welcome_survey_selection'),
    url(r'^introduction_selection/', views.introduction_selection, name='introduction_selection'),
    url(r'^survey_selection/', views.survey_selection, name='survey_selection'),
    url(r'^selection_gil_save_clicks/', views.selection_gil_save_clicks, name='selection_gil_save_clicks'),
    url(r'^selection_save_task/', views.selection_save_task, name='selection_save_task'),
    url(r'^save_session_start_time/', views.save_session_start_time, name='save_session_start_time'),
    url(r'^end_screen/', views.end_screen, name='end_screen'),
    url(r'^save_pilot_mode_session_start_time/', views.save_pilot_mode_session_start_time, name='save_pilot_mode_session_start_time'),
    url(r'^welcome_pilot_mode/', views.welcome_pilot_mode, name='welcome_pilot_mode'),
    url(r'^introduction_pilot_mode/', views.introduction_pilot_mode, name='introduction_pilot_mode'),
    url(r'^save_pilot_mode_task/', views.save_pilot_mode_task, name='save_pilot_mode_task'),
    url(r'^pilot_mode/', views.pilot_mode, name='pilot_mode')
]
