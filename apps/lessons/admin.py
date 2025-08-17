# apps/lessons/admin.py
from django.contrib import admin
from .models import Tag, Exercise, ExerciseAttempt

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "kind", "cefr_level", "created_at")
    search_fields = ("prompt",)
    list_filter = ("kind", "cefr_level", "created_at")
    filter_horizontal = ("tags",)

@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "exercise", "session", "turn", "score", "created_at")
    list_filter = ("created_at",)
