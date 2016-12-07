from django.shortcuts import render


def interface(request):
    return render(request, 'exp/../login/templates/login.html')