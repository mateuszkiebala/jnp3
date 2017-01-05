from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from forms import RegistrationForm
from models import UserProfile


def home(request):
    return render(request, 'login.html')


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        if user.is_active and user.is_superuser:
            return HttpResponseRedirect('/accounts/admin_loggedin')
        else:
            return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def admin_loggedin(request):
    return HttpResponseRedirect('/admin/')


def loggedin(request):
    return render_to_response('interface.html',
                              {'user': request.user})


def invalid_login(request):
    return render_to_response('invalid_login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile(user=user,
                        name=form.cleaned_data['username'],
                        age=form.cleaned_data['age'],
                        gender=form.cleaned_data['gender']).save()
            return HttpResponseRedirect('/accounts/register_success')
        else:
            args['form'] = form
            return render_to_response('register.html', args)

    args['form'] = RegistrationForm()
    return render_to_response('register.html', args)


def register_success(request):
    return render_to_response('register_success.html')