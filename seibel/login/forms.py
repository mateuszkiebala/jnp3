from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    age = forms.IntegerField(required=True, min_value=0, max_value=150, label=_("Age"))

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(required=True, choices=GENDER_CHOICES)


def clean_username(self):
    try:
        user = User.objects.get(username__iexact=self.cleaned_data['username'])
    except User.DoesNotExist:
        return self.cleaned_data['username']
    raise forms.ValidationError(_("The username already exists. Please try another one."))