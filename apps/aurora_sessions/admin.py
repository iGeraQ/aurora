# apps/sessions/admin.py
from django.contrib import admin
from .models import PracticeSession, Turn, AudioClip

@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "started_at", "ended_at", "cefr_level", "lang_code")
    search_fields = ("id", "user__username")
    list_filter = ("cefr_level", "lang_code", "started_at")

@admin.register(Turn)
class TurnAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "created_at", "asr_confidence", "user_audio_ms", "tts_ms")
    search_fields = ("id", "user_text", "agent_text")
    list_filter = ("created_at",)

@admin.register(AudioClip)
class AudioClipAdmin(admin.ModelAdmin):
    list_display = ("id", "turn", "clip_type", "duration_ms", "mime_type", "created_at")
    list_filter = ("clip_type", "created_at")
