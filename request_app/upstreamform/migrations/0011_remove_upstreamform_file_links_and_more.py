# Generated by Django 5.0.6 on 2024-07-15 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0010_upstreamform_file_links_upstreamform_file_paths'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upstreamform',
            name='file_links',
        ),
        migrations.RemoveField(
            model_name='upstreamform',
            name='file_paths',
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='file_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='file_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
