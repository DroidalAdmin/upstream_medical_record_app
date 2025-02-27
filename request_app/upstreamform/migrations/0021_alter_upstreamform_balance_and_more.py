# Generated by Django 5.0.6 on 2024-07-18 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0020_upstreamform_invoice_pdf_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upstreamform',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc10_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc1_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc2_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc3_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc4_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc5_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc6_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc7_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc8_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='misc9_path',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='upstreamform',
            name='total_pages',
            field=models.IntegerField(default=0),
        ),
    ]
