from django.db import models
from ConferenceApp.models import Conference
from django.core.validators import RegexValidator

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="sessions")
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\s]+$',
                message="Le nom de la salle ne doit contenir que des lettres, chiffres et espaces."
            )
        ]
    )