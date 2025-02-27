# Generated by Django 5.0.1 on 2024-06-27 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CasForm',
            fields=[
                ('casid', models.AutoField(db_column='casid', primary_key=True, serialize=False)),
                ('Claim_ID', models.CharField(db_column='Claim_ID', max_length=255)),
                ('Insurance', models.CharField(db_column='Insurance', max_length=255)),
                ('Facility', models.CharField(db_column='Facility', max_length=255)),
                ('Charge_From_Date', models.CharField(db_column='Charge_From_Date', max_length=20)),
                ('Charge_To_Date', models.CharField(db_column='Charge_To_Date', max_length=20)),
                ('Facility_NPI', models.CharField(db_column='Facility_NPI', max_length=255)),
                ('Primary_Member_ID', models.CharField(db_column='Primary_Member_ID', max_length=255)),
                ('Charge_Debit_Amount', models.CharField(db_column='Charge_Debit_Amount', max_length=20)),
                ('Pat_Primary_Payer_Name', models.CharField(db_column='Pat_Primary_Payer_Name', max_length=255)),
                ('Patient_Full_Name', models.CharField(db_column='Patient_Full_Name', max_length=255)),
                ('Patient_Birthday', models.CharField(db_column='Patient_Birthday', max_length=20)),
                ('Current_Billing_Status', models.CharField(db_column='Current_Billing_Status', max_length=255)),
                ('Claim_Number', models.CharField(db_column='Claim_Number', max_length=255)),
                ('Patient_Account_Number', models.CharField(db_column='Patient_Account_Number', max_length=255)),
                ('UHC_Availity_ClaimStatus', models.CharField(db_column='UHC_Availity_ClaimStatus', max_length=255)),
                ('Total_BilledAmount', models.CharField(db_column='Total_BilledAmount', max_length=20)),
                ('Total_Paid', models.CharField(db_column='Total_Paid', max_length=20)),
                ('Total_Adjustment', models.CharField(db_column='Total_Adjustment', max_length=20)),
                ('Total_Patient_Responsibility', models.CharField(db_column='Total_Patient_Responsibility', max_length=20)),
                ('Service_Code', models.CharField(db_column='Service_Code', max_length=255)),
                ('Billing_Amount', models.CharField(db_column='Billing_Amount', max_length=20)),
                ('Allowed_Amount', models.CharField(db_column='Allowed_Amount', max_length=20)),
                ('Paid_Amount', models.CharField(db_column='Paid_Amount', max_length=20)),
                ('Check_Number', models.CharField(db_column='Check_Number', max_length=255)),
                ('Check_Date', models.CharField(db_column='Check_Date', max_length=20)),
                ('Remark_Code', models.CharField(db_column='Remark_Code', max_length=255)),
                ('Category_1', models.CharField(db_column='Category_1', max_length=255)),
                ('Status_1', models.CharField(db_column='Status_1', max_length=255)),
                ('Description_1', models.CharField(db_column='Description_1', max_length=255)),
                ('Status_Description_1', models.CharField(db_column='Status_Description_1', max_length=255)),
                ('Claim_Reason_Code_1', models.CharField(db_column='Claim_Reason_Code_1', max_length=255)),
                ('Category_2', models.CharField(db_column='Category_2', max_length=255)),
                ('Status_2', models.CharField(db_column='Status_2', max_length=255)),
                ('Description_2', models.CharField(db_column='Description_2', max_length=255)),
                ('Status_Description_2', models.CharField(db_column='Status_Description_2', max_length=255)),
                ('Claim_Reason_Code_2', models.CharField(db_column='Claim_Reason_Code_2', max_length=255)),
                ('Category_3', models.CharField(db_column='Category_3', max_length=255)),
                ('Status_3', models.CharField(db_column='Status_3', max_length=255)),
                ('Description_3', models.CharField(db_column='Description_3', max_length=255)),
                ('Status_Description_3', models.CharField(db_column='Status_Description_3', max_length=255)),
                ('Bot_Status', models.CharField(db_column='Bot_Status', max_length=255)),
                ('Comments', models.CharField(db_column='Comments', max_length=255)),
                ('Updated_By', models.CharField(db_column='Updated_By', max_length=255)),
                ('RCM_Comments', models.CharField(db_column='RCM_Comments', max_length=255)),
                ('cas_assigned_name', models.CharField(db_column='cas_assigned_name', max_length=255)),
                ('cas_status', models.CharField(db_column='cas_status', max_length=20)),
                ('cas_assigned_to', models.CharField(db_column='cas_assigned_to', max_length=20)),
            ],
            options={
                'db_table': 'casform',
                'managed': True,
            },
        ),
    ]
