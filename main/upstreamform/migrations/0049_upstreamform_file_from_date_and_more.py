# Generated by Django 5.1 on 2024-09-18 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0048_upstreamform_patient_from_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='upstreamform',
            name='file_from_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='file_to_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
