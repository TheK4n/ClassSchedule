from django.contrib import admin
from table.models import Exercise, ClassGroup


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["name", "weekday", "time_start", "teacher", "auditory",
                    "parity", "group"]
    ordering = ("group", "weekday", "time_start")


class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ("name",)


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ClassGroup, ClassGroupAdmin)
