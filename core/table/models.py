from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Exercise(models.Model):
    class Parity(models.TextChoices):
        EVEN = "EVE", "Чет"
        ODD = "ODD", "Нечет"
        COMMON = "COM", "Общее"

    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Понедельник"
        TUESDAY = 1, "Вторник"
        WEDNESDAY = 2, "Среда"
        THURSDAY = 3, "Четверг"
        FRIDAY = 4, "Пятница"
        SATURDAY = 5, "Суббота"

    id = models.BigAutoField(primary_key=True)
    weekday = models.IntegerField(
        null=False,
        choices=Weekday.choices,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    name = models.CharField(max_length=80)
    time_start = models.TimeField()
    teacher = models.CharField(max_length=80)
    auditory = models.CharField(max_length=20)
    parity = models.CharField(
        max_length=3,
        choices=Parity.choices,
        default=Parity.COMMON,
    )

