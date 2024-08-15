from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Department)
admin.site.register(models.Disease)
admin.site.register(models.Patient)
admin.site.register(models.Doctor)
admin.site.register(models.MedicationCategory)
admin.site.register(models.Medication)
admin.site.register(models.Prescription)
admin.site.register(models.Visit)
admin.site.register(models.StaffPosition)
admin.site.register(models.Staff)