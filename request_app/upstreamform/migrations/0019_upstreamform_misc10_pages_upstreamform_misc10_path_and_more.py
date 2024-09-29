# Generated by Django 5.0.6 on 2024-07-18 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0018_remove_upstreamform_misc10_pages_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='upstreamform',
            name='misc10_pages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='misc10_path',
            field=models.TextField(blank=True, db_column='misc10_path', null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='misc7_pages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='misc7_path',
            field=models.TextField(blank=True, db_column='misc7_path', null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='misc8_pages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='misc8_path',
            field=models.TextField(blank=True, db_column='misc8_path', null=True),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='misc9_pages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='misc9_path',
            field=models.TextField(blank=True, db_column='misc9_path', null=True),
        ),
    ]
