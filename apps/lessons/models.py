# apps/lessons/models.py
import uuid
from django.db import models

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, max_length=64)
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Exercise(models.Model):
    TYPE_PROMPT = "prompt"     # roleplay / diálogo
    TYPE_FILLGAP = "fillgap"   # completar
    TYPE_CHOICE = "choice"     # opción múltiple
    TYPE_PRON = "pron"         # práctica de pronunciación (frases, trabalenguas)
    TYPE_FREE = "free"         # producción libre guiada

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kind = models.CharField(
        max_length=10,
        choices=[(TYPE_PROMPT,"prompt"), (TYPE_FILLGAP,"fillgap"), (TYPE_CHOICE,"choice"), (TYPE_PRON,"pron"), (TYPE_FREE,"free")],
        default=TYPE_PROMPT
    )
    cefr_level = models.CharField(
        max_length=3,
        choices=[("A1","A1"),("A2","A2"),("B1","B1"),("B2","B2"),("C1","C1"),("C2","C2")],
        default="A2"
    )
    prompt = models.TextField()               # Consigna o texto base
    answer = models.TextField(null=True, blank=True)  # Respuesta esperada (si aplica)
    data = models.JSONField(default=dict, blank=True) # Opciones, choices, hints, etc.

    tags = models.ManyToManyField(Tag, related_name="exercises", blank=True)

    # Embedding para similaridad (elige UNO de los dos enfoques):
    # 1) Con pgvector:
    # embedding = VectorField(dim=768, null=True, blank=True)
    # 2) Si aún no usas pgvector: guarda binario o base64 y luego migras:
    embedding_blob = models.BinaryField(null=True, blank=True, editable=False)    

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        preview = (self.prompt[:50] + "…") if len(self.prompt) > 50 else self.prompt
        return f"[{self.cefr_level}] {preview}"


class ExerciseAttempt(models.Model):
    """
    Intento del usuario sobre un ejercicio (ata a una sesión/turno si quieres).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="attempts")
    session = models.ForeignKey("aurora_sessions.PracticeSession", on_delete=models.CASCADE, related_name="exercise_attempts")
    turn = models.ForeignKey("aurora_sessions.Turn", null=True, blank=True, on_delete=models.SET_NULL, related_name="exercise_attempts")

    user_text = models.TextField(null=True, blank=True)
    agent_feedback = models.JSONField(default=dict, blank=True)  # gramática, semántica, pronunciación
    score = models.FloatField(null=True, blank=True)  # puntuación 0..1 o 0..100

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
