from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class ClassGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


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
    group = models.ForeignKey(ClassGroup, on_delete=models.PROTECT)
    weekday = models.IntegerField(
        null=False,
        choices=Weekday.choices,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    time_start = models.TimeField()
    name = models.CharField(max_length=80)
    teacher = models.CharField(max_length=80)
    auditory = models.CharField(max_length=20)
    parity = models.CharField(
        max_length=3,
        choices=Parity.choices,
        default=Parity.COMMON,
    )

    def __str__(self):
        return self.name

