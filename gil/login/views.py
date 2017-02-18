from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template.context_processors import csrf
from models import UserProfile
from forms import RegistrationForm
from django.contrib import auth
from django.contrib.auth.models import User
import copy


@csrf_protect
def login_experiment(request):
    args = {}
    args['mode'] = 'experiment'
    args.update(csrf(request))
    if request.method == "POST":
        data = copy.copy(request.POST)
        password = 'sdjlkghdsjhglkhu4hgo384g4h83hgl834g'
        data['password1'] = password
        data['password2'] = password
        form = RegistrationForm(data)
        if form.is_valid():
            selection_mode = get_selection_mode()
            user = form.save()
            UserProfile(user=user,
                        name=form.cleaned_data['username'],
                        age=form.cleaned_data['age'],
                        gender=form.cleaned_data['gender'],
                        selection_mode=selection_mode).save()
            username = data.get('username', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/welcome_training_gil/')
        else:
            args['form'] = form
            return render_to_response('login.html', args)

    args['form'] = RegistrationForm()
    return render_to_response('login.html', args)


@csrf_protect
def login_pilot_mode(request):
    args = {}
    args['mode'] = 'pilot_mode'
    args.update(csrf(request))
    if request.method == "POST":
        data = copy.copy(request.POST)
        password = 'sdjlkghdsjhglkhu4hgo384g4h83hgl834g'
        data['password1'] = password
        data['password2'] = password
        form = RegistrationForm(data)
        if form.is_valid():
            selection_mode = get_selection_mode()
            user = form.save()
            UserProfile(user=user,
                        name=form.cleaned_data['username'],
                        age=form.cleaned_data['age'],
                        gender=form.cleaned_data['gender'],
                        selection_mode=selection_mode).save()
            username = data.get('username', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/welcome_pilot_mode/')
        else:
            args['form'] = form
            return render_to_response('login.html', args)

    args['form'] = RegistrationForm()
    return render_to_response('login.html', args)


MODES = 3
ADMINS = 1


def get_selection_mode():
    cnt = User.objects.all().count()
    if ((cnt - ADMINS) % MODES) == 0:
        selection_mode = 'I.TB'
    elif ((cnt - ADMINS) % MODES) == 1:
        selection_mode = 'II.TB'
    elif ((cnt - ADMINS) % MODES) == 2:
        selection_mode = 'III.TB'
    return selection_mode

