# Generated by Django 5.0.6 on 2024-07-17 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0013_upstreamform_misc1_pages_upstreamform_misc2_pages_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upstreamform',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='total_pages',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
