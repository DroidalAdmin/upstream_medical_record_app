# Generated by Django 5.0.7 on 2024-08-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0025_alter_upstreamform_ev_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upstreamform',
            name='ev_status',
            field=models.CharField(blank=True, db_column='ev_status', default='New', max_length=100, null=True),
        ),
    ]
