from django.contrib.auth.models import User
from django.db import models

import random
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length = 255, primary_key = True)
    about = models.TextField()
    duty = models.TextField()
    rooms = models.IntegerField()
    meterage = models.IntegerField()
    staff_numbers = models.IntegerField()

    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length = 255, primary_key=True)
    about = models.TextField()

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    national_code = models.IntegerField(unique=True)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, blank=True, null=True) 
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    is_ok = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    national_code = models.IntegerField(unique=True)
    number = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"
    

class MedicationCategory(models.Model):
    name = models.CharField(max_length = 255, primary_key = True)
    about = models.TextField()

    def __str__(self):
        return self.name

class Medication(models.Model):
    name = models.CharField(max_length = 255, primary_key = True)
    about = models.TextField()
    how_to_use = models.TextField()
    effects = models.CharField(max_length = 255)
    med_type = models.ForeignKey(MedicationCategory, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    meds = models.ManyToManyField(Medication, related_name = 'prescriptions')
    text = models.TextField()
    how_to_use = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"Prescription for {self.patient} by {self.doctor} on {self.date}"

class Visit(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    date = models.DateTimeField()
    is_confirmed = models.BooleanField(default = False)
    text = models.TextField()

    def __str__(self):
        return f"Visit on {self.date} by {self.doctor}"

class StaffPosition(models.Model):
    name = models.CharField(max_length = 255, primary_key = True)
    about = models.TextField()

    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_num = models.IntegerField()
    national_code = models.IntegerField(unique=True)
    number = models.IntegerField()
    position = models.ForeignKey(StaffPosition, on_delete=models.CASCADE)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



