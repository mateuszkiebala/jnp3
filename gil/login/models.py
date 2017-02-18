from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default="noname", max_length=50)
    age = models.IntegerField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    selection_mode = models.CharField(default='-', max_length=50)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])