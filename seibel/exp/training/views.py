from django.shortcuts import render
from exp.models import UserSessions, UserSettings, ExpPanel
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.http import HttpResponse


def training(request):
    settings_set = UserSettings.objects.filter(user=request.user)
    if settings_set.__len__() > 0:
        user_settings = settings_set[0]
        exp_panel = ExpPanel.objects.filter(feedback_type=user_settings.feedback_type,
                                            timer_type=user_settings.timer_type)
        return render(request, 'game.html',
                      {'game_type': 'Training',
                       'feedback_type': user_settings.feedback_type,
                       'timer_type': user_settings.timer_type,
                       'time_gap': user_settings.time_gap,
                       'instr': exp_panel[0].instr,
                       'time_to_start': exp_panel[0].time_to_start
                       })
    else:
        return render(request, 'no_settings.html')


@csrf_protect
@login_required()
@api_view(['POST', ])
def update_training(request):
    if request.method == 'POST':
        json_data = request.data
        UserSessions.objects.filter(user=request.user,
                                    feedback_type=json_data['feedback_type'],
                                    timer_type=json_data['timer_type']
                                    ).update(training_done='Yes')
        return HttpResponse("Training info updated.")
