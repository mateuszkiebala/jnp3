from django.shortcuts import render, render_to_response
from exp.models import UserSettings, UserResult, UserSessions, UserSessionsInfo
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.http import HttpResponse
from datetime import datetime


def play(request):
    user_settings_set = UserSettings.objects.filter(user=request.user)
    if user_settings_set.__len__() > 0:
        user_settings = user_settings_set[0]
        latest_session_set = UserSessions.objects.filter(user=request.user,
                                                         feedback_type=user_settings.feedback_type,
                                                         timer_type=user_settings.timer_type)
        if latest_session_set.__len__() > 0:
            user_session = latest_session_set[0]
            latest_session_no = latest_session_set[0].session_number
        else:
            latest_session_no = 0
            user_session = UserSessions(user=request.user,
                                        feedback_type=user_settings.feedback_type,
                                        timer_type=user_settings.timer_type,
                                        training_done='No',
                                        session_number=0)
            user_session.save()

        confs_done = [r.configuration for r in UserResult.objects.filter(user=request.user,
                                                                          session_number=latest_session_no,
                                                                          feedback_type=user_settings.feedback_type,
                                                                          timer_type=user_settings.timer_type)]
        return render(request, 'game.html',
                        {'game_type': 'Normal',
                         'session_limit': user_settings.session_limit,
                         'feedback_type': user_settings.feedback_type,
                         'timer_type': user_settings.timer_type,
                         'time_gap': user_settings.time_gap,
                         'session_number': latest_session_no,
                         'training_done': user_session.training_done,
                         'confs_done': confs_done })
    else:
        return render(request, 'no_settings.html')


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


@csrf_protect
@login_required()
@api_view(['POST', ])
def update_session_start(request):
    if request.method == 'POST':
        json_data = request.data
        UserSessionsInfo(user=request.user,
                         feedback_type=json_data['feedback_type'],
                         timer_type=json_data['timer_type'],
                         session_number=json_data['session_number'],
                         start=json_data['start']).save()
        return HttpResponse("Session start updated")


@csrf_protect
@login_required()
@api_view(['POST', ])
def update_session_end(request):
    if request.method == 'POST':
        json_data = request.data
        UserSessionsInfo.objects.filter(user=request.user,
                                        feedback_type=json_data['feedback_type'],
                                        timer_type=json_data['timer_type'],
                                        session_number=json_data['session_number']
                                        ).update(end=json_data['end'])

        sessions = UserSessionsInfo.objects.filter(user=request.user,
                                                feedback_type=json_data['feedback_type'],
                                                timer_type=json_data['timer_type'],
                                                session_number=json_data['session_number'])

        if sessions.__len__() > 0:
            start = sessions[0].start
            end = sessions[0].end
            time = end - start
            UserSessionsInfo.objects.filter(user=request.user,
                                            feedback_type=json_data['feedback_type'],
                                            timer_type=json_data['timer_type'],
                                            session_number=json_data['session_number']
                                            ).update(time=time)
            return HttpResponse("Session end updated")
        else:
            return HttpResponse("Session end update failed.")