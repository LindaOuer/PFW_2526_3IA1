from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from ConferenceApp.models import Conference

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
                message="Room name should only contain letters, numbers, and spaces."
            )
        ]
    )
    def clean(self):
        if self.conference and self.session_day:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError(
                    {"session_day": "must be within the conference dates."}
                )

        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError(
                    {"end_time": "must be later than start time."}
                )
    def __str__(self):
        return f"{self.title} ({self.conference.name})"