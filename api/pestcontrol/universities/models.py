from django.utils.timezone import now
from django.db import models
from django.db.models.fields import URLField


class University(models.Model):
    class UniversityStatus(models.TextChoices):
        HIRING = "Hiring"
        FREEZE = "Hiring Freeze"
        LAYOFFS = "Layoffs"

    name = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=50, choices=UniversityStatus.choices, default=UniversityStatus.HIRING
    )
    last_update = models.DateTimeField(default=now, editable=True)
    application_link = URLField(
        blank=True,
    )
    notes = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
