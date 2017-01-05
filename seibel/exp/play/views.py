from django.shortcuts import render, render_to_response
from exp.models import UserSettings, UserResult, UserSessions
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.http import HttpResponse


def play(request):
    user_settings = UserSettings.objects.get(user=request.user)
    latest_session_set = UserSessions.objects.filter(user=request.user,
                                                     feedback_type=user_settings.feedback_type,
                                                     timer_type=user_settings.timer_type)

    if latest_session_set.__len__() > 0:
        latest_session = latest_session_set[0].session_number
    else:
        latest_session = 0
        UserSessions(user=request.user,
                     feedback_type=user_settings.feedback_type,
                     timer_type=user_settings.timer_type,
                     session_number=0).save()

    confs_done =  [r.configuration for r in UserResult.objects.filter(user=request.user,
                                                                      session_number=latest_session,
                                                                      feedback_type=user_settings.feedback_type,
                                                                      timer_type=user_settings.timer_type)]
    return render(request, 'game.html',
                    {'game_type': 'Normal',
                     'session_limit': user_settings.session_limit,
                     'feedback_type': user_settings.feedback_type,
                     'timer_type': user_settings.timer_type,
                     'time_gap': user_settings.time_gap,
                     'session_number': latest_session,
                     'confs_done': confs_done })


@csrf_protect
@login_required()
@api_view(['POST', ])
def update_results(request):
    if request.method == 'POST':
        json_data = request.data
        UserResult(user=request.user,
                   feedback_type=json_data['feedback_type'],
                   timer_type=json_data['timer_type'],
                   session_number=int(json_data['session_number']),
                   configuration=int(json_data['configuration']),
                   start_time=json_data['start_time'],
                   end_time=json_data['end_time'],
                   total_time=json_data['total_time'],
                   errors_count=int(json_data['errors_count']),
                   is_correct=json_data['is_correct'],
                   bulb_1=json_data['bulb_1'],
                   bulb_2=json_data['bulb_2'],
                   bulb_3=json_data['bulb_3'],
                   bulb_4=json_data['bulb_4'],
                   bulb_5=json_data['bulb_5'],
                   bulb_6=json_data['bulb_6'],
                   bulb_7=json_data['bulb_7'],
                   bulb_8=json_data['bulb_8'],
                   bulb_9=json_data['bulb_9'],
                   bulb_10=json_data['bulb_10'],
                   fin_1=json_data['fin_1'],
                   fin_2=json_data['fin_2'],
                   fin_3=json_data['fin_3'],
                   fin_4=json_data['fin_4'],
                   fin_5=json_data['fin_5'],
                   fin_6=json_data['fin_6'],
                   fin_7=json_data['fin_7'],
                   fin_8=json_data['fin_8'],
                   fin_9=json_data['fin_9'],
                   fin_10=json_data['fin_10']
                   ).save()
        return HttpResponse("Results updated.")


@csrf_protect
@login_required()
@api_view(['POST', ])
def update_session(request):
    if request.method == 'POST':
        json_data = request.data
        UserSessions.objects.filter(user=request.user,
                                    feedback_type=json_data['feedback_type'],
                                    timer_type=json_data['timer_type']
                                    ).update(session_number=int(json_data['session_number']) + 1)

        return HttpResponse("Session updated.")

