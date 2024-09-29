# Generated by Django 5.0.1 on 2024-06-27 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UpstreamForm',
            fields=[
                ('request_id', models.AutoField(db_column='request_id', primary_key=True, serialize=False)),
                ('request_date', models.CharField(db_column='request_date', max_length=20)),
                ('med_record_no', models.CharField(db_column='med_record_no', max_length=255)),
                ('last_name', models.CharField(db_column='last_name', max_length=255)),
                ('first_name', models.CharField(db_column='first_name', max_length=255)),
                ('mi', models.CharField(db_column='mi', max_length=255)),
                ('request_type', models.CharField(db_column='request_type', max_length=255)),
                ('status', models.CharField(db_column='status', max_length=255)),
                ('encounter', models.CharField(db_column='encounter', max_length=255)),
                ('status_date', models.CharField(db_column='status_date', max_length=20)),
                ('time', models.CharField(db_column='time', max_length=20)),
                ('copies_due', models.CharField(db_column='copies_due', max_length=20)),
                ('disclosure_method', models.CharField(db_column='disclosure_method', max_length=255)),
                ('purpose', models.TextField(db_column='purpose')),
                ('birthdate', models.CharField(db_column='birthdate', max_length=20)),
                ('fax_number', models.CharField(db_column='fax_number', max_length=255)),
                ('ssn', models.CharField(db_column='ssn', max_length=255)),
                ('optional_info', models.TextField(db_column='optional_info')),
                ('requestor', models.CharField(db_column='requestor', max_length=255)),
                ('company_no', models.CharField(db_column='company_no', max_length=255)),
                ('company', models.CharField(db_column='company', max_length=255)),
                ('address1', models.CharField(db_column='address1', max_length=255)),
                ('address2', models.CharField(db_column='address2', max_length=255)),
                ('city', models.CharField(db_column='city', max_length=255)),
                ('state', models.CharField(db_column='state', max_length=255)),
                ('zip_code', models.CharField(db_column='zip_code', max_length=255)),
                ('phone', models.CharField(db_column='phone', max_length=255)),
                ('ext', models.CharField(db_column='ext', max_length=255)),
                ('fax', models.CharField(db_column='fax', max_length=255)),
                ('email', models.CharField(db_column='email', max_length=255)),
                ('tpo', models.CharField(db_column='tpo', max_length=255)),
                ('medicare', models.CharField(db_column='medicare', max_length=255)),
                ('suspend', models.CharField(db_column='suspend', max_length=255)),
                ('empl_open', models.CharField(db_column='empl_open', max_length=255)),
                ('time_opened', models.CharField(db_column='time_opened', max_length=20)),
                ('empl_close', models.CharField(db_column='empl_close', max_length=255)),
                ('close_date', models.CharField(db_column='close_date', max_length=20)),
                ('time_closed', models.CharField(db_column='time_closed', max_length=20)),
                ('cng_open_time', models.CharField(db_column='cng_open_time', max_length=20)),
                ('cng_close_time', models.CharField(db_column='cng_close_time', max_length=20)),
                ('invoice_no', models.CharField(db_column='invoice_no', max_length=255)),
                ('balance', models.CharField(db_column='balance', max_length=20)),
                ('paper_copy_pages', models.CharField(db_column='paper_copy_pages', max_length=20)),
                ('other_pages', models.CharField(db_column='other_pages', max_length=20)),
                ('notes', models.TextField(db_column='notes')),
                ('approve_doc_path', models.CharField(db_column='approve_doc_path', max_length=255)),
                ('approve_doc_status', models.CharField(db_column='approve_doc_status', max_length=10)),
                ('ev_createddatetime', models.CharField(blank=True, db_column='ev_createddatetime', max_length=100, null=True)),
                ('ev_assigned_createddatetime', models.CharField(blank=True, db_column='ev_assigned_createddatetime', max_length=100, null=True)),
                ('ev_closed_createddatetime', models.CharField(blank=True, db_column='ev_closed_createddatetime', max_length=100, null=True)),
                ('ev_remarks', models.CharField(blank=True, db_column='ev_remarks', max_length=50, null=True)),
                ('ev_status', models.CharField(blank=True, db_column='ev_status', max_length=50, null=True)),
                ('ev_assigned_to', models.CharField(blank=True, db_column='ev_assigned_to', max_length=10, null=True)),
                ('ev_assigned_name', models.CharField(blank=True, db_column='ev_assigned_name', max_length=100, null=True)),
                ('misc1_path', models.TextField(db_column='misc1_path')),
                ('misc2_path', models.TextField(db_column='misc2_path')),
                ('misc3_path', models.TextField(db_column='misc3_path')),
                ('misc4_path', models.TextField(db_column='misc4_path')),
                ('misc5_path', models.TextField(db_column='misc5_path')),
                ('misc6_path', models.TextField(db_column='misc6_path')),
            ],
            options={
                'db_table': 'upstremform',
            },
        ),
    ]