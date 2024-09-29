# Generated by Django 5.1 on 2024-08-30 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0041_charginglist_email_charginglist_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upstreamform',
            name='address1',
            field=models.CharField(blank=True, db_column='address1', max_length=255),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='address2',
            field=models.CharField(blank=True, db_column='address2', max_length=255),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='city',
            field=models.CharField(blank=True, db_column='city', max_length=255),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='company',
            field=models.CharField(blank=True, db_column='company', max_length=255),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='invoice_no',
            field=models.CharField(blank=True, db_column='invoice_no', max_length=255),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='zip_code',
            field=models.CharField(blank=True, db_column='zip_code', max_length=255),
        ),
    ]