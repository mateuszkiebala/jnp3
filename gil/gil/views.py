from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse


def main_menu(request):
    return render(request, 'main_menu.html')

