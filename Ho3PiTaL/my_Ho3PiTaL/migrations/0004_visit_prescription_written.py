# Generated by Django 5.1 on 2024-08-16 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_Ho3PiTaL', '0003_remove_patient_department_remove_patient_disease_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='prescription_written',
            field=models.BooleanField(default=False),
        ),
    ]