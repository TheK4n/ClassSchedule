from django.contrib import admin
from schedule.models import Exercise, ClassGroup


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["name", "group", "weekday", "time_start", "teacher", "auditory",
                    "parity"]
    ordering = ("group", "weekday", "time_start")


class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ("name",)


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ClassGroup, ClassGroupAdmin)
