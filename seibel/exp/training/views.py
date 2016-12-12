from django.shortcuts import render


def training(request):
    return render(request, 'training.html')


def feedback(request):
    return render(request, 'train_feedback.html')


def nonFeedback(request):
    return render(request, 'train_non_feedback.html')


def timeLimited(request, feedback_type):
    return render(request, 'game.html',
                  {'game_type': 'training',
                   'feedback_type': feedback_type,
                   'time_type': 'time_limited'}
                  )


def timeless(request, feedback_type):
    return render(request, 'game.html',
                  {'game_type': 'training',
                   'feedback_type': feedback_type,
                   'time_type': 'timeless'})


def game(request):
    return render(request, 'game.html')
