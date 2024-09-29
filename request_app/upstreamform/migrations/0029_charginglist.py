# Generated by Django 5.1 on 2024-08-23 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0028_alter_upstreamform_notes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('base_fare', models.CharField(blank=True, max_length=255, null=True)),
                ('flat_fee', models.CharField(blank=True, max_length=255, null=True)),
                ('free_for', models.CharField(blank=True, max_length=255, null=True)),
                ('per_page', models.CharField(blank=True, max_length=255, null=True)),
                ('fee_limit', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_5', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_10', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_20', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_25', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_30', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_40', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_50', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_80', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_100', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_150', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_250', models.CharField(blank=True, max_length=255, null=True)),
                ('page_1_to_1000', models.CharField(blank=True, max_length=255, null=True)),
                ('page_2_to_30', models.CharField(blank=True, max_length=255, null=True)),
                ('page_2_to_200', models.CharField(blank=True, max_length=255, null=True)),
                ('page_11_to_20', models.CharField(blank=True, max_length=255, null=True)),
                ('page_11_to_40', models.CharField(blank=True, max_length=255, null=True)),
                ('page_11_to_50', models.CharField(blank=True, max_length=255, null=True)),
                ('page_21_to_30', models.CharField(blank=True, max_length=255, null=True)),
                ('page_21_to_40', models.CharField(blank=True, max_length=255, null=True)),
                ('page_21_to_50', models.CharField(blank=True, max_length=255, null=True)),
                ('page_21_to_60', models.CharField(blank=True, max_length=255, null=True)),
                ('page_21_to_100', models.CharField(blank=True, max_length=255, null=True)),
                ('page_21_to_500', models.CharField(blank=True, max_length=255, null=True)),
                ('page_26_to_100', models.CharField(blank=True, max_length=255, null=True)),
                ('page_26_to_350', models.CharField(blank=True, max_length=255, null=True)),
                ('page_31_to_100', models.CharField(blank=True, max_length=255, null=True)),
                ('page_101_to_200', models.CharField(blank=True, max_length=255, null=True)),
                ('above_5_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_10_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_20_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_25_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_30_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_40_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_50_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_60_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_80_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_100_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_150_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_200_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_250_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_350_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_500_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('above_1000_pages', models.CharField(blank=True, max_length=255, null=True)),
                ('required_fee', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('optional_fee', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_1', models.CharField(blank=True, max_length=255, null=True)),
                ('optional_fee_1', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_2', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'charging_list',
            },
        ),
    ]
