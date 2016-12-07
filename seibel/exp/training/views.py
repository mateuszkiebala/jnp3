from django.shortcuts import render


def training(request):
    return render(request, 'training.html')


def feedback(request):
    return render(request, 'feedback.html')


def nonFeedback(request):
    return render(request, 'non_feedback.html')


def game(request):
    return render(request, 'game.html')
