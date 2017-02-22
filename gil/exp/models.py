from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SessionSettings(models.Model):
    pause = models.PositiveIntegerField()
    training_gil_session_time = models.PositiveIntegerField(default=0)
    survey_gil_session_time = models.PositiveIntegerField(default=0)
    training_selection_session_time = models.PositiveIntegerField(default=0)
    training_tasks = models.TextField(default=[])

    def clean(self):
        if self._state.adding and DescriptionSettings.objects.all().exists():
            raise ValidationError('Settings already exists.')


class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    top_description = models.TextField()
    bottom_description = models.TextField()
    rule = models.TextField()
    card_choice_description = models.TextField(default="")
    card_P = models.TextField()
    card_nP = models.TextField()
    card_Q = models.TextField()
    card_nQ = models.TextField()
    correct_answers = models.TextField()


class SelectionResults(models.Model):
    user = models.ForeignKey(User)
    external_task_number = models.PositiveIntegerField(default=1)
    task_id = models.PositiveIntegerField()
    cards_order = models.TextField(default=[])
    correctness = models.CharField(default="-", max_length=20)
    correct_cards = models.TextField(default=[])
    start_time = models.PositiveIntegerField(default=0)
    doing_task_time = models.CharField(default='-', max_length=20)
    solving_task_time = models.CharField(default='-', max_length=20)
    card_P_clicks = models.TextField(default='[]')
    card_nP_clicks = models.TextField(default='[]')
    card_Q_clicks = models.TextField(default='[]')
    card_nQ_clicks = models.TextField(default='[]')
    card_P_final = models.CharField(null=True, max_length=100)
    card_nP_final = models.CharField(null=True, max_length=100)
    card_Q_final = models.CharField(null=True, max_length=100)
    card_nQ_final = models.CharField(null=True, max_length=100)
    chosen_cards = models.TextField(null=True)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value


class GilResults(models.Model):
    user = models.ForeignKey(User)
    SESSION_CHOICES = (
        ('Training GIL', 'Training GIL'),
        ('Survey GIL', 'Survey GIL'),
        ('Training Selection', 'Training Selection'),
        ('Survey Selection', 'Survey Selection'),
    )
    session_type = models.CharField(max_length=100, choices=SESSION_CHOICES)
    task_id = models.PositiveIntegerField()
    clicks = models.TextField(null=True)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value


class DescriptionSettings(models.Model):
    welcome_description = models.TextField()
    training_gil_description = models.TextField()
    survey_gil_description = models.TextField()
    training_selection_description = models.TextField()
    survey_selection_description = models.TextField()
    ending_description = models.TextField()

    def clean(self):
        if self._state.adding and DescriptionSettings.objects.all().exists():
            raise ValidationError('Settings already exists.')


class UserTasks(models.Model):
    user = models.ForeignKey(User)
    tasks = models.TextField()
    done = models.PositiveIntegerField(default=0)


class PilotModeSettings(models.Model):
    welcome_description = models.TextField()
    training_tasks = models.TextField(default=[])

    def clean(self):
        if self._state.adding and DescriptionSettings.objects.all().exists():
            raise ValidationError('Settings already exists.')


class PilotModeResults(models.Model):
    user = models.ForeignKey(User)
    external_task_number = models.PositiveIntegerField(default=1)
    task_id = models.PositiveIntegerField()
    cards_order = models.TextField(default=[])
    correctness = models.CharField(default="-", max_length=20)
    correct_cards = models.TextField(default=[])
    start_time = models.PositiveIntegerField(default=0)
    doing_task_time = models.CharField(default='-', max_length=20)
    solving_task_time = models.CharField(default='-', max_length=20)
    card_P_clicks = models.TextField(default='[]')
    card_nP_clicks = models.TextField(default='[]')
    card_Q_clicks = models.TextField(default='[]')
    card_nQ_clicks = models.TextField(default='[]')
    card_P_final = models.CharField(null=True, max_length=100)
    card_nP_final = models.CharField(null=True, max_length=100)
    card_Q_final = models.CharField(null=True, max_length=100)
    card_nQ_final = models.CharField(null=True, max_length=100)
    chosen_cards = models.TextField(null=True)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

