# Generated by Django 5.1 on 2024-09-11 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0047_upstreamform_invoice_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='upstreamform',
            name='patient_from_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='patient_to_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]