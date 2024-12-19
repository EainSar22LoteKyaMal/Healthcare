from django.db import models
from authapp.models import CustomUser

class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    name = models.CharField(max_length=225, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    ph_num = models.CharField(max_length=15, null=False, blank=False, unique=True)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"
    
class MedicalForm(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_form')
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    doctor = models.CharField(max_length=255)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.doctor}"
