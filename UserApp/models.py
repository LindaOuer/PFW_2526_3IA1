from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# Create your models here.

nameValidator = RegexValidator(r'^[A-Za-z\s]+$', 'Only alphabetic characters are allowed.')

def validateEmail(value):
    allowed_domains = ['esprit.tn', 'univ.tn', 'mit.edu', 'ox.ad.uk']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(f'Email domain must be one of the following: {", ".join(allowed_domains)}')

class User(AbstractUser):
    ROLE_CHOICES = [
    ("participant", "Participant"),
    ("committee", "Organizing Committee Member")
    ]
    user_id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
    first_name = models.CharField(max_length=150, blank=True, validators=[nameValidator])
    last_name = models.CharField(max_length=150, blank=True, validators=[nameValidator])
    email = models.EmailField(unique=True, validators=[validateEmail])
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="participant")
    nationality = models.CharField(max_length=100, blank=True, null=True)