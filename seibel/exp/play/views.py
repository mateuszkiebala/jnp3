from django.shortcuts import render, render_to_response


def play(request):
    return render(request, 'play.html')


def feedback(request):
    return render(request, 'play_feedback.html')


def nonFeedback(request):
    return render(request, 'play_non_feedback.html')


def timeLimited(request, feedback_type):
    return render(request, 'game.html',
                  {'game_type': 'play',
                   'feedback_type': feedback_type,
                   'time_type': 'time_limited'}
                  )


def timeless(request, feedback_type):
    return render(request, 'game.html',
                  {'game_type': 'play',
                   'feedback_type': feedback_type,
                   'time_type': 'timeless'})


def game(request):
    return render(request, 'game.html')