# Generated by Django 5.0.6 on 2024-07-09 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0004_upstreamform_disclosure_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='upstreamform',
            name='external_request_createddatetime',
            field=models.CharField(blank=True, db_column='external_request_createddatetime', max_length=100, null=True),
        ),
    ]
