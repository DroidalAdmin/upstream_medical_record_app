# Generated by Django 5.0.6 on 2024-07-15 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0011_remove_upstreamform_file_links_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='upstreamform',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='upstreamform',
            name='total_pages',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]