from django.contrib import admin
from table.models import Exercise


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["name", "weekday", "time_start", "teacher", "parity"]
    ordering = ('weekday', "time_start")

admin.site.register(Exercise, ExerciseAdmin)
