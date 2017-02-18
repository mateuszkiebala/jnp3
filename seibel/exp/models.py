from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Create your models here.


class UserSettings(models.Model):
    user = models.ForeignKey(User)
    session_limit = models.IntegerField()

    FEEDBACK_TYPE_CHOICES = (
        ('Non_feedback', 'Non_feedback'),
        ('Feedback', 'Feedback'),
    )
    feedback_type = models.CharField(default=FEEDBACK_TYPE_CHOICES[0], max_length=100, choices=FEEDBACK_TYPE_CHOICES)

    TIMER_CHOICES = (
        ('Timeless', 'Timeless'),
        ('Time_limited', 'Time_limited'),
    )
    timer_type = models.CharField(default=TIMER_CHOICES[0], max_length=100, choices=TIMER_CHOICES)
    time_gap = models.PositiveIntegerField(default=5000, validators=[MinValueValidator(1000)])

    def clean(self):
        if self._state.adding and UserSettings.objects.filter(user=self.user).exists():
            raise ValidationError('Settings for this user already exists.')

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value


class UserResult(models.Model):
    user = models.ForeignKey(User)
    feedback_type = models.CharField(max_length=100, default='Feedback')
    timer_type = models.CharField(max_length=100, default='Timeless')
    session_number = models.IntegerField(default=0)
    configuration = models.IntegerField(default=0)
    start_time = models.CharField(default="-", max_length=100)
    end_time = models.CharField(default="-", max_length=100)
    total_time = models.CharField(default="0s", max_length=100)
    errors_count = models.IntegerField(default=0)
    is_correct = models.CharField(max_length=10, default='Nie')
    bulb_1 = models.CharField(max_length=10, default='Nie')
    bulb_2 = models.CharField(max_length=10, default='Nie')
    bulb_3 = models.CharField(max_length=10, default='Nie')
    bulb_4 = models.CharField(max_length=10, default='Nie')
    bulb_5 = models.CharField(max_length=10, default='Nie')
    bulb_6 = models.CharField(max_length=10, default='Nie')
    bulb_7 = models.CharField(max_length=10, default='Nie')
    bulb_8 = models.CharField(max_length=10, default='Nie')
    bulb_9 = models.CharField(max_length=10, default='Nie')
    bulb_10 = models.CharField(max_length=10, default='Nie')
    fin_1 = models.CharField(max_length=10, default='-')
    fin_2 = models.CharField(max_length=10, default='-')
    fin_3 = models.CharField(max_length=10, default='-')
    fin_4 = models.CharField(max_length=10, default='-')
    fin_5 = models.CharField(max_length=10, default='-')
    fin_6 = models.CharField(max_length=10, default='-')
    fin_7 = models.CharField(max_length=10, default='-')
    fin_8 = models.CharField(max_length=10, default='-')
    fin_9 = models.CharField(max_length=10, default='-')
    fin_10 = models.CharField(max_length=10, default='-')

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def __unicode__(self):
        return unicode(self.user)

    @staticmethod
    def get_done_configurations(_user, _session_number):
        results = UserResult.objects.filter(user=_user, session_number=_session_number)
        return [r.configuration for r in results]


class UserSessions(models.Model):
    user = models.ForeignKey(User)
    session_number = models.IntegerField(default=0)
    feedback_type = models.CharField(default='Feedback', max_length=100)
    timer_type = models.CharField(default='Timeless', max_length=100)
    training_done = models.CharField(default='No', max_length=10)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value


class UserSessionsInfo(models.Model):
    user = models.ForeignKey(User)
    session_number = models.IntegerField(default=0)
    feedback_type = models.CharField(default='Feedback', max_length=100)
    timer_type = models.CharField(default='Timeless', max_length=100)
    start = models.DateTimeField(auto_now_add=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    time = models.CharField(default="-", max_length=100)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value


class ExpPanel(models.Model):
    instr = models.TextField()
    time_to_start = models.IntegerField(default=5000)

    FEEDBACK_TYPE_CHOICES = (
        ('Non_feedback', 'Non_feedback'),
        ('Feedback', 'Feedback'),
    )
    feedback_type = models.CharField(default=FEEDBACK_TYPE_CHOICES[0], max_length=100, choices=FEEDBACK_TYPE_CHOICES)

    TIMER_CHOICES = (
        ('Timeless', 'Timeless'),
        ('Time_limited', 'Time_limited'),
    )
    timer_type = models.CharField(default=TIMER_CHOICES[0], max_length=100, choices=TIMER_CHOICES)
