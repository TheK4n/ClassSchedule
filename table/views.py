import datetime
from typing import Literal

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from core.settings import REVERSE_PARITY, DEBUG
from .models import Exercise, ClassGroup
from .converters import DateConverter


def get_weekday_name(weekday: int) -> str:
    return [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ][weekday]


def inverse_parity(parity: Literal["EVE", "ODD"]) -> Literal["ODD", "EVE"]:
    d: dict[Literal["EVE", "ODD"], Literal["ODD", "EVE"]] = {
        "EVE": "ODD",
        "ODD": "EVE"
    }
    return d[parity]


def get_week_parity(date: datetime.date) -> Literal["EVE", "ODD"]:
    is_even = date.isocalendar().week % 2 == 0
    parity = "EVE" if is_even else "ODD"

    if REVERSE_PARITY:
        return inverse_parity(parity)
    return parity


def get_parity_name(parity: Literal["EVE", "ODD"]) -> Literal["Чет", "Нечет"]:
    d: dict[Literal["EVE", "ODD"], Literal["Чет", "Нечет"]] = {
        "EVE": "Чет",
        "ODD": "Нечет"
    }
    return d[parity]


def get_weekday(date: datetime.date) -> Literal[0, 1, 2, 3, 4, 5, 6]:
    return date.weekday()


def render_groups(request: WSGIRequest):
    groups = ClassGroup.objects.all()
    return render(request, 'groups.html', {
        "host": request.get_host(),
        "groups": groups,
        "DEBUG": DEBUG,
    })


def get_exercises_by_weekday_and_by_group(weekday: int, parity: Literal["EVE", "ODD"], group: ClassGroup) -> list[Exercise]:
    q = Q(parity=parity) | Q(parity="COM")

    return list(Exercise.objects \
        .filter(group=group) \
        .filter(weekday=weekday) \
        .filter(q) \
        .order_by('time_start'))


def get_exercises_by_date_and_by_group(date: datetime.date, group: ClassGroup) -> list[Exercise]:
    weekday = get_weekday(date)
    week_parity = get_week_parity(date)

    return get_exercises_by_weekday_and_by_group(weekday, week_parity, group)


def get_all_groups(_: WSGIRequest):
    res = {"groups": []}

    for group in ClassGroup.objects.all():
        res["groups"].append(group.name)

    return JsonResponse(res)


def get_table_by_date(request: WSGIRequest, group_name: str, date: datetime.date):
    group = get_object_or_404(ClassGroup, name=group_name)

    exercises = get_exercises_by_date_and_by_group(date, group)

    weekday = get_weekday(date)
    weekday_name = get_weekday_name(weekday)
    week_parity = get_week_parity(date)

    res = {"weekday": weekday_name, "week_parity": week_parity,  "exercises": []}

    for exercise in exercises:
        res["exercises"].append({
            "name": exercise.name,
            "time_start": exercise.time_start,
            "teacher": exercise.teacher,
            "auditory": exercise.auditory,
        })

    return JsonResponse(res)


def render_date(request: WSGIRequest, group_name: str, date: datetime.date):
    group = get_object_or_404(ClassGroup, name=group_name)

    today_exercises = get_exercises_by_date_and_by_group(date, group)

    current_weekday_name = get_weekday_name(date.weekday())
    current_parity = get_week_parity(date)
    current_parity_name = get_parity_name(current_parity)

    next_day = date + datetime.timedelta(days=1)

    return render(request, 'today.html', {
        "host": request.get_host(),
        "weekday_name": current_weekday_name,
        "parity_name": current_parity_name,
        "exercises": today_exercises,
        "group": group,
        "next_date": next_day,
        "DEBUG": DEBUG,
    })


def render_today(request: WSGIRequest, group_name: str):
    today = datetime.date.today()
    return render_date(request, group_name, today)
