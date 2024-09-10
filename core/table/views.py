import datetime

from django.shortcuts import render
from django.db.models import Q

from core.settings import REVERSE_PARITY
from .models import Exercise


def is_current_week_parity_even() -> bool:
    current_week_number = datetime.datetime.now().isocalendar().week
    current_parity = current_week_number % 2 == 0

    return not current_parity if REVERSE_PARITY else current_parity


def not_parity(parity: str) -> str:
    if parity == "ODD":
        return "EVE"
    else:
        return "ODD"


def today(request):
    weekday = request.GET.get("weekday", None)
    parity = request.GET.get("parity", None)

    if weekday is None:
        current_week_day = datetime.datetime.now().weekday()
    else:
        current_week_day = int(weekday)

    if current_week_day > 5:
        current_week_day = 5
    elif current_week_day < 0:
        current_week_day = 0


    current_week_day_name = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ][current_week_day]

    if parity is None:
        current_parity = "EVE" if is_current_week_parity_even() else "ODD"
    else:
        current_parity = parity

    q = Q(parity=current_parity) | Q(parity="COM")

    exercises = Exercise.objects.filter(weekday=current_week_day).filter(q).order_by('time_start')

    current_parity_name = "Чет" if current_parity == "EVE" else "Нечет"

    next_weekday = 0 if current_week_day == 5 else current_week_day + 1

    return render(request, 'today.html', {
        "host": request.get_host(),
        "weekday_name": current_week_day_name,
        "next_weekday": next_weekday,
        "parity": current_parity,
        "parity_name": current_parity_name,
        "next_parity": not_parity(parity) if next_weekday == 0 else current_parity,
        "exercises": exercises,
        "group": "2611",
    })

