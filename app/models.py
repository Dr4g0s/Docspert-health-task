from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from app.managers import CustomUserManager
from app.utils import get_upload_path


class Patient(AbstractBaseUser, PermissionsMixin):
    """Default user model for online medical consultations App."""

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Investigation(models.Model):
    """Represents a medical investigation done by the 
    patient and uploaded to the system"""

    patient = models.ForeignKey(Patient, related_name='investigations', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=get_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Consultation(models.Model):
    """Represents an online medical consultation
    created by a patient"""

    patient = models.ForeignKey(Patient, related_name='consultations', on_delete=models.CASCADE)
    investigations = models.ManyToManyField(Investigation)
    speciality = models.CharField(max_length=150)
    complaint = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.speciality
