from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from UserApp.models import User
# Create your models here.
class Conference(models.Model):
    THEMES = [
        ('CS', 'Computer Science'),
        ('AI', 'Artificial Intelligence'),
        ('SE', 'Science & Engineering'),
        ('SSE', 'Social Sciences & Education'),
        ('IT', 'Interdisciplinary Themes'),
    ]
    
    name = models.CharField(max_length=200, validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s]+$',
                message="The conference name should only contain letters and spaces."
            )
        ])
    theme = models.CharField(max_length=50, choices=THEMES)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(validators=[MinLengthValidator(30, "Description must be at least 30 characters long.")])
    def __str__ (self):
        return self.name
    
    def clean(self):
        if self.start_date is None or self.end_date is None:
            raise ValidationError("Start date and end date must be provided.")
        if self.end_date <= self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")
    
    
def validate_keywords(value):
    keywords_list = [k.strip() for k in value.split(",") if k.strip()]
    if len(keywords_list) > 10:
        raise ValidationError("Vous ne pouvez pas avoir plus de 10 mots-clés.")
    return value

class Submission(models.Model):
    STATUS_CHOICES = [
    ("submitted", "Submitted"),
    ("under_review", "Under Review"),
    ("accepted", "Accepted"),
    ("rejected", "Rejected"),
    ]

    submission_id = models.CharField(max_length=20, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    keywords = models.TextField()
    paper = models.FileField(
        upload_to="papers/", validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    submission_date = models.DateField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="submissions")
    

    def clean(self):
        
        if self.conference:
            if now().date() > self.conference.start_date:
                raise ValidationError("Only submissions allowed are for upcoming conferences.")

        # Vérifier nombre max de soumissions par jour (3 par utilisateur)
        if self.user and self.submission_date:
            count_submissions_today = Submission.objects.filter(
                user=self.user,
                submission_date=self.submission_date
            ).exclude(pk=self.pk).count()
            if count_submissions_today >= 3:
                raise ValidationError("A user can submit a maximum of 3 submissions per day.")
    def save(self, *args, **kwargs):
        if not self.submission_id:
            self.submission_id = "SUB-" + get_random_string(8).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
class OrganizingCommittee(models.Model):
    ROLE_CHOICES = [
    ("chair", "Chair"),
    ("co-chair", "Co-chair"),
    ("committee", "Organizing Committee Member"),
]
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="committee_members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="committees")
    committee_role = models.CharField(max_length=100,choices=ROLE_CHOICES,default="comite")
    date_joined = models.DateField(auto_now_add=True)