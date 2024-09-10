import datetime
from typing import Literal

from django.shortcuts import render
from django.db.models import Q

from core.settings import REVERSE_PARITY
from .models import Exercise


def get_current_week() -> int:
    return datetime.datetime.now().isocalendar().week


def get_current_weekday() -> int:
    return datetime.datetime.now().weekday()


def not_parity(parity: Literal["EVE"] | Literal["ODD"]) -> Literal["EVE"] | Literal["ODD"]:
    if parity == "ODD":
        return "EVE"
    else:
        return "ODD"


def get_week_parity(weekday: int) -> Literal["EVE"] | Literal["ODD"]:
    current_parity = weekday % 2 == 0
    if REVERSE_PARITY:
        return "EVE" if current_parity else "ODD"
    else:
        return "ODD" if current_parity else "EVE"


def validate_week_day(weekday: int) -> int:
    if weekday > 5:
        return 5
    elif weekday < 0:
        return 0
    return weekday


def get_week_day_name_from_number(weekday: int) -> str:
    return [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ][weekday]


def get_week_parity_name(parity: Literal["EVE"] | Literal["ODD"]) -> Literal["Чет"] | Literal["Нечет"]:
    return "Чет" if parity == "EVE" else "Нечет"


def get_next_weekday(weekday: int):
    return 0 if weekday == 5 else weekday + 1


def get_exercises_by_weekday(weekday: int) -> list[Exercise]:
    parity = get_week_parity(weekday)
    q = Q(parity=parity) | Q(parity="COM")

    return list(Exercise.objects \
        .filter(weekday=weekday) \
        .filter(q) \
        .order_by('time_start'))



def today(request):
    weekday = request.GET.get("weekday", None)
    parity = request.GET.get("parity", None)

    if weekday is None:
        current_weekday: int = get_current_weekday()
    else:
        current_weekday: int = int(weekday)

    current_weekday = validate_week_day(current_weekday)
    current_weekday_name = get_week_day_name_from_number(current_weekday)

    if parity is None:
        current_parity = get_week_parity(current_weekday)
    else:
        current_parity = parity

    exercises = get_exercises_by_weekday(current_weekday)

    current_parity_name = get_week_parity_name(current_parity)

    next_weekday = get_next_weekday(current_weekday)

    return render(request, 'today.html', {
        "host": request.get_host(),
        "weekday_name": current_weekday_name,
        "next_weekday": next_weekday,
        "parity": current_parity,
        "parity_name": current_parity_name,
        "next_parity": not_parity(parity) if next_weekday == 0 else current_parity,
        "exercises": exercises,
        "group": "2611",
    })

