# Generated by Django 5.0.6 on 2024-07-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0002_request_remove_upstreamform_disclosure_method_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Request',
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='patient_date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='patient_first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='patient_last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='request_file',
            field=models.FileField(blank=True, null=True, upload_to='requests/'),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='requestor_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='requestor_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='request_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]