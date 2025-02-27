# Generated by Django 5.1 on 2024-08-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0036_charginglist'),
    ]

    operations = [
        migrations.AddField(
            model_name='charginglist',
            name='each_additional_hour',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='charginglist',
            name='fee_limit_for_electronic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='charginglist',
            name='fee_limit_for_mail',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='charginglist',
            name='first_hour',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
