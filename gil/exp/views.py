from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from exp.models import DescriptionSettings, SessionSettings, GilResults, Tasks, UserTasks, SelectionResults, PilotModeSettings, PilotModeResults
from login.models import UserProfile
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
import numpy
import re
from random import shuffle


def welcome(request):
    general_settings = DescriptionSettings.objects.all()[0]
    return render(request, 'welcome.html',
                  {'description': general_settings.welcome_description})


@login_required()
def welcome_training_gil(request):
    general_settings = DescriptionSettings.objects.all()[0]
    return render(request, 'welcome_training_gil.html',
                  {'description': general_settings.training_gil_description})


@login_required()
def training_gil(request):
    args = {}
    settings = SessionSettings.objects.all()[0]
    args['training_gil_session_time'] = settings.training_gil_session_time
    args['pause'] = settings.pause
    args['session_type'] = 'Training GIL'
    return render(request, 'gil.html', args)


@login_required()
def welcome_survey_gil(request):
    general_settings = DescriptionSettings.objects.all()[0]
    return render(request, 'welcome_survey_gil.html',
                  {'description': general_settings.survey_gil_description})


@login_required()
def survey_gil(request):
    args = {}
    settings = SessionSettings.objects.all()[0]
    args['survey_gil_session_time'] = settings.survey_gil_session_time
    args['pause'] = settings.pause
    args['session_type'] = 'Survey GIL'
    return render(request, 'gil.html', args)


@csrf_protect
@login_required()
@api_view(['POST', ])
def survey_gil_save_clicks(request):
    if request.method == 'POST':
        update_clicks(request, 'Survey GIL')
        return HttpResponse("Session updated")


@login_required()
def welcome_training_selection(request):
    general_settings = DescriptionSettings.objects.all()[0]
    return render(request, 'welcome_training_selection.html',
                  {'description': general_settings.training_selection_description})


@login_required()
def training_selection(request):
    settings = SessionSettings.objects.all()[0]
    args = {}
    args['training_selection_session_time'] = settings.training_selection_session_time
    args['pause'] = settings.pause
    args['session_type'] = 'Training Selection'
    return render(request, 'selection.html', args)


@login_required()
def welcome_survey_selection(request):
    order_user_tasks(request.user)
    next_task, task_number = get_next_task(request.user)
    return render(request, 'welcome_survey_selection.html',
                  {'task_number': next_task})


@login_required()
def introduction_selection(request):
    args = get_task_args(request.user)
    args['task_number'], task_number = get_next_task(request.user)
    return render(request, 'introduction_selection.html', args)


@csrf_protect
@login_required()
@api_view(['POST', ])
def save_session_start_time(request):
    if request.method == 'POST':
        json_data = request.data
        task_done, task_id = get_next_task(request.user)
        training_tasks_count = len(get_training_tasks())
        if task_done > training_tasks_count:
            SelectionResults(user=request.user,
                            task_id=task_id,
                            start_time=json_data['start_time']).save()
        return HttpResponse("Session updated")


@login_required()
def survey_selection(request):
    args = get_task_args(request.user)
    settings = SessionSettings.objects.all()[0]
    args['task_number'], task_number = get_next_task(request.user)
    args['survey_selection_session_time'] = settings.survey_selection_session_time
    args['pause'] = settings.pause
    args['tasks_count'] = Tasks.objects.all().count()
    args['session_type'] = 'Survey Selection'
    return render(request, 'selection.html', args)


CARD_NAMES = ['P', 'nP', 'Q', 'nQ']


def get_task_args(user):
    task_done, task_id = get_next_task(user)
    task_res = Tasks.objects.filter(id=task_id)
    selection_mode = UserProfile.objects.filter(user=user)[0].selection_mode
    args = {}
    args['selection_mode'] = selection_mode
    cards_order = shuffle_cards()
    if task_res.count() > 0:
        task = task_res[0]
        args['top_description'] = task.top_description
        args['bottom_description'] = task.bottom_description
        args['rule'] = task.rule
        args['card_choice_description'] = task.card_choice_description
        args['cards_order'] = cards_order
        for i in range(0, 4):
            set_cards(args, task, cards_order, i)
    return args


def set_cards(args, task, cards_order, id):
    name = 'card_' + str(CARD_NAMES[cards_order[id]])
    card_id = 'card_' + str(id)
    args[card_id] = getattr(task, name)


def shuffle_cards():
    s = range(0, 4)
    shuffle(s)
    return s


def get_training_tasks():
    ss = SessionSettings.objects.all()
    if ss.count() > 0:
        training_tasks = ss[0].training_tasks
    else:
        training_tasks = ""
    return [int(i) for i in re.findall('[0-9]+', training_tasks)]


def order_user_tasks(user, training_tasks=get_training_tasks()):
    if UserTasks.objects.filter(user=user).count() == 0:
        n = Tasks.objects.all().count()
        if n == 0:
            task_ids = []
        else:
            task_ids = [x for x in range(1, n+1) if x not in training_tasks]
            shuffle(task_ids)
        task_ids = training_tasks + task_ids # training tasks have to be in concrete order
        UserTasks(user=user,
                  tasks=task_ids,
                  done=0).save()


def get_next_task(user):
    user_tasks = UserTasks.objects.filter(user=user)
    n = Tasks.objects.all().count()
    if user_tasks.count() > 0:
        tasks_done = user_tasks[0].done
        task_number = int(re.findall('[0-9]+', user_tasks[0].tasks)[min(tasks_done, n - 1)])
    else:
        tasks_done = 0
        task_number = 1
    return tasks_done + 1, task_number


@csrf_protect
@login_required()
@api_view(['POST', ])
def selection_gil_save_clicks(request):
    if request.method == 'POST':
        task_done, task_id = get_next_task(request.user)
        training_tasks_count = len(get_training_tasks())
        if task_done > training_tasks_count:
            update_clicks(request, 'Survey Selection', task_id)
        return HttpResponse("Session updated")


@csrf_protect
@login_required()
@api_view(['POST', ])
def selection_save_task(request):
    if request.method == 'POST':
        json_data = request.data
        task_done, task_id = get_next_task(request.user)
        training_tasks_count = len(get_training_tasks())
        # training tasks doesnt count to results
        if task_done > training_tasks_count:
            res = SelectionResults.objects.filter(user=request.user,
                                                  task_id=task_id)[0]
            task = Tasks.objects.filter(id=task_id)[0]
            cards_order = json_data['cards_order']
            chosen_cards = [CARD_NAMES[cards_order[id]] for id in json_data['chosen_cards']]
            doing_task_time = int(json_data['session_end_time']) - int(res.start_time)
            solving_task_time = int(json_data['session_end_time'] - int(json_data['session_start_time']))

            result = re.findall("[A-Z]|[a-z][A-Z]", str(task.correct_answers))
            correctness = True if len(set(result) - set(chosen_cards)) == 0 and\
                                  len(set(chosen_cards) - set(result)) == 0 else False

            clicks = []
            for i in range(0, 4):
                get_card_clicks(clicks, json_data, i)

            cards_order_names = [CARD_NAMES[i] for i in cards_order]

            SelectionResults.objects.filter(user=request.user,
                                            task_id=task_id).\
                                            update(doing_task_time=doing_task_time,
                                                   solving_task_time=solving_task_time,
                                                   cards_order = cards_order_names,
                                                   correctness=correctness,
                                                   correct_cards=task.correct_answers,
                                                   card_P_clicks=clicks[cards_order_names.index('P')],
                                                   card_nP_clicks=clicks[cards_order_names.index('nP')],
                                                   card_Q_clicks=clicks[cards_order_names.index('Q')],
                                                   card_nQ_clicks=clicks[cards_order_names.index('nQ')],
                                                   card_P_final=json_data['card_' + str(cards_order_names.index('P')) + '_final'],
                                                   card_nP_final=json_data['card_' + str(cards_order_names.index('nP')) + '_final'],
                                                   card_Q_final=json_data['card_' + str(cards_order_names.index('Q')) + '_final'],
                                                   card_nQ_final=json_data['card_' + str(cards_order_names.index('nQ')) + '_final'],
                                                   chosen_cards=chosen_cards)

        UserTasks.objects.filter(user=request.user).update(done=task_done)
        return HttpResponse("Session updated")


def get_card_clicks(clicks, json_data, id):
    name = 'card_' + str(id) + '_clicks'
    c = json_data[name]
    clicks.append(numpy.cumsum([c[i + 1] - c[i] for i in range(0, len(c) - 1)])
                  if len(c) > 1 else [])


@login_required()
def end_screen(request):
    general_settings = DescriptionSettings.objects.all()[0]
    return render(request, 'end_screen.html',
                  {'description': general_settings.ending_description})


def update_clicks(request, session_type, task_id=0):
    json_data = request.data
    if session_type == 'Survey GIL':
        results_set = GilResults.objects.filter(user=request.user,
                                                session_type=session_type)
    else:
        results_set = GilResults.objects.filter(user=request.user,
                                                session_type=session_type,
                                                task_id=task_id)
    c = json_data['clicks']
    clicks = numpy.cumsum([c[i + 1] - c[i] for i in range(0, len(c) - 1)])
    if results_set.__len__() > 0:
        results_set.update(clicks=clicks)
    else:
        GilResults(user=request.user,
                   session_type=session_type,
                   task_id=task_id,
                   clicks=clicks).save()


# -------- PILOT MODE -------- #


@csrf_protect
@login_required()
@api_view(['POST', ])
def save_pilot_mode_session_start_time(request):
    if request.method == 'POST':
        json_data = request.data
        task_done, task_id = get_next_task(request.user)
        training_tasks_count = len(get_pilot_mode_training_tasks())
        if task_done > training_tasks_count:
            PilotModeResults(user=request.user,
                             task_id=task_id,
                             start_time=json_data['start_time']).save()
        return HttpResponse("Session updated")


@csrf_protect
@login_required()
@api_view(['POST', ])
def save_pilot_mode_task(request):
    if request.method == 'POST':
        json_data = request.data
        task_done, task_id = get_next_task(request.user)
        training_tasks_count = len(get_pilot_mode_training_tasks())
        # training tasks doesnt count to results
        if task_done > training_tasks_count:
            res = PilotModeResults.objects.filter(user=request.user,
                                                  task_id=task_id)[0]
            task = Tasks.objects.filter(id=task_id)[0]
            cards_order = json_data['cards_order']
            chosen_cards = [CARD_NAMES[cards_order[id]] for id in json_data['chosen_cards']]
            doing_task_time = int(json_data['session_end_time']) - int(res.start_time)
            solving_task_time = int(json_data['session_end_time'] - int(json_data['session_start_time']))

            result = re.findall("[A-Z]|[a-z][A-Z]", str(task.correct_answers))
            correctness = True if len(set(result) - set(chosen_cards)) == 0 and\
                                  len(set(chosen_cards) - set(result)) == 0 else False

            clicks = []
            for i in range(0, 4):
                get_card_clicks(clicks, json_data, i)

            cards_order_names = [CARD_NAMES[i] for i in cards_order]

            PilotModeResults.objects.filter(user=request.user,
                                            task_id=task_id).\
                                            update(doing_task_time=doing_task_time,
                                                   solving_task_time=solving_task_time,
                                                   cards_order = cards_order_names,
                                                   correctness=correctness,
                                                   correct_cards=task.correct_answers,
                                                   card_P_clicks=clicks[cards_order_names.index('P')],
                                                   card_nP_clicks=clicks[cards_order_names.index('nP')],
                                                   card_Q_clicks=clicks[cards_order_names.index('Q')],
                                                   card_nQ_clicks=clicks[cards_order_names.index('nQ')],
                                                   card_P_final=json_data['card_' + str(cards_order_names.index('P')) + '_final'],
                                                   card_nP_final=json_data['card_' + str(cards_order_names.index('nP')) + '_final'],
                                                   card_Q_final=json_data['card_' + str(cards_order_names.index('Q')) + '_final'],
                                                   card_nQ_final=json_data['card_' + str(cards_order_names.index('nQ')) + '_final'],
                                                   chosen_cards=chosen_cards)

        UserTasks.objects.filter(user=request.user).update(done=task_done)
        return HttpResponse("Session updated")


@login_required()
def welcome_pilot_mode(request):
    order_user_tasks(request.user, get_pilot_mode_training_tasks())
    next_task, task_number = get_next_task(request.user)
    return render(request, 'welcome_pilot_mode.html',
                  {'task_number': next_task})


@login_required()
def introduction_pilot_mode(request):
    args = get_task_args(request.user)
    args['task_number'], task_number = get_next_task(request.user)
    return render(request, 'introduction_pilot_mode.html', args)


def get_pilot_mode_training_tasks():
    training_tasks = PilotModeSettings.objects.all()[0].training_tasks
    return [int(i) for i in re.findall('[0-9]+', training_tasks)]


@login_required()
def pilot_mode(request):
    args = get_task_args(request.user)
    args['task_number'], task_number = get_next_task(request.user)
    args['tasks_count'] = Tasks.objects.all().count()
    return render(request, 'pilot_mode.html', args)
