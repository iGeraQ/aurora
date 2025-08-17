# apps/sessions/models.py
import uuid
from django.db import models
from django.conf import settings

USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

class PracticeSession(models.Model):
    """
    Una sesión de práctica (conversación). Agrupa múltiples turnos.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="practice_sessions"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    cefr_level = models.CharField(
        max_length=3, null=True, blank=True,
        choices=[("A1","A1"),("A2","A2"),("B1","B1"),("B2","B2"),("C1","C1"),("C2","C2")]
    )
    lang_code = models.CharField(max_length=16, default="en-US")  # idioma del ASR/TTS
    meta = models.JSONField(default=dict, blank=True)  # config de la sesión (voz, sample rate, etc.)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"Session {self.id} ({self.user or 'anon'})"


class Turn(models.Model):
    """
    Un intercambio: lo que dijo el usuario y la respuesta del agente.
    """
    ROLE_USER = "user"
    ROLE_AGENT = "agent"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(PracticeSession, on_delete=models.CASCADE, related_name="turns")
    created_at = models.DateTimeField(auto_now_add=True)

    # Texto final del ASR (del usuario) y texto del agente
    user_text = models.TextField(null=True, blank=True)
    agent_text = models.TextField(null=True, blank=True)

    # Confianza del ASR, duración estimada del audio del usuario, etc.
    asr_confidence = models.FloatField(null=True, blank=True)
    user_audio_ms = models.IntegerField(null=True, blank=True)
    tts_ms = models.IntegerField(null=True, blank=True)

    # Feedback de gramática / estilo (LanguageTool, etc.)
    grammar_feedback = models.JSONField(default=list, blank=True)
    # Feedback de pronunciación (scores por fonema/palabra si lo agregas)
    pronunciation = models.JSONField(default=dict, blank=True)

    # Sugerencias de estudio/ejercicios mostradas en ese turno
    suggestions = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Turn {self.id} in {self.session_id}"


class AudioClip(models.Model):
    """
    Guarda referencias a audio asociado a un turno (entrada del usuario o TTS).
    Útil si quieres reproducir o auditar después.
    """
    TYPE_USER = "user"
    TYPE_TTS = "tts"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name="audio_clips")
    clip_type = models.CharField(max_length=8, choices=[(TYPE_USER,"user"), (TYPE_TTS,"tts")])
    # Puedes usar FileField y un backend S3 con django-storages
    file = models.FileField(upload_to="sessions/audio/", null=True, blank=True)
    # O almacenar un “preview” corto en base64 para depurar (no recomendado para audio largo)
    preview_b64 = models.TextField(null=True, blank=True)
    duration_ms = models.IntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=64, default="audio/ogg")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.clip_type} audio for turn {self.turn_id}"
