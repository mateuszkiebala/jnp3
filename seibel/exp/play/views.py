from django.shortcuts import render


def play(request):
    return render(request, 'play.html')


def feedback(request):
    return render(request, 'feedback.html')


def nonFeedback(request):
    return render(request, 'non_feedback.html')


def game(request):
    return render(request, 'game.html')