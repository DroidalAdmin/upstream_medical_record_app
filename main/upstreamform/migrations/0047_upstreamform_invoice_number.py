# Generated by Django 5.1 on 2024-09-06 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0046_requestfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='upstreamform',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
