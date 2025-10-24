from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

import uuid

def validate_academic_email(value):
    allowed_domains = ["esprit.tn", "univ.tn", "mit.edu", "ox.ac.uk"]  
    domain = value.split("@")[-1]
    if domain not in allowed_domains:
        raise ValidationError(
            f"L'adresse email doit appartenir à un domaine universitaire valide."
        )
name_validator = RegexValidator(
    regex=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s-]+$',
    message="Ce champ ne doit contenir que des lettres, espaces ou tirets."
)
def generate_user_id():
    # Génère un identifiant unique du type user-XXXXXX (6 caractères alphanumériques)
    return "user" + uuid.uuid4().hex[:4].upper()
class User(AbstractUser):
    ROLE_CHOICES = [
    ("participant", "Participant"),
    ("committee", "Organizing Committee Member")
]
    user_id = models.CharField(max_length=8, primary_key=True, unique=True,
        editable=False)
    first_name = models.CharField(max_length=150, blank=True,validators=[name_validator])
    last_name = models.CharField(max_length=150, blank=True,validators=[name_validator])
    email = models.EmailField(unique=True,validators=[validate_academic_email])
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="participant")
    nationality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def save(self, *args, **kwargs):
        if not self.user_id:  
            new_id = generate_user_id()
            
            while User.objects.filter(user_id=new_id).exists():
                new_id = generate_user_id()
            self.user_id = new_id
        super().save(*args, **kwargs)