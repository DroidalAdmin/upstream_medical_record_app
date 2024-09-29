from django.db import models

# Create your models here.

class RequestFile(models.Model):
    request = models.ForeignKey('UpstreamForm', on_delete=models.CASCADE, related_name='files')
    file_path = models.FileField(upload_to='media/Auth/')

    class Meta:
        db_table = 'requestfile'

class UpstreamForm(models.Model):
    request_id = models.AutoField(primary_key=True, db_column='request_id')
    request_date = models.CharField(max_length=20, db_column='request_date', blank=True,null=True)
    request_date2 = models.CharField(max_length=20, db_column='request_date2', blank=True,null=True)
    med_record_no = models.CharField(max_length=255, db_column='med_record_no', blank=True,null=True)
    last_name = models.CharField(max_length=255, db_column='last_name', blank=True,null=True)
    first_name = models.CharField(max_length=255, db_column='first_name', blank=True,null=True)
    mi = models.CharField(max_length=255, db_column='mi', blank=True,null=True)
    request_type = models.CharField(max_length=255, db_column='request_type', blank=True,null=True)
    status = models.CharField(max_length=255, db_column='status', blank=True,null=True)
    encounter = models.CharField(max_length=255, db_column='encounter', blank=True,null=True)
    status_date = models.CharField(max_length=20, db_column='status_date', blank=True,null=True)
    time = models.CharField(max_length=20, db_column='time', blank=True,null=True)
    copies_due = models.CharField(max_length=20, db_column='copies_due', blank=True,null=True)
    disclosure_method = models.CharField(max_length=255, db_column='disclosure_method',blank=True,null=True)
    purpose = models.TextField(db_column='purpose', blank=True,null=True)
    birthdate = models.CharField(max_length=20, db_column='birthdate', blank=True,null=True)
    fax_number = models.CharField(max_length=255, db_column='fax_number', blank=True,null=True)
    ssn = models.CharField(max_length=255, db_column='ssn', blank=True,null=True)
    optional_info = models.TextField(db_column='optional_info', blank=True,null=True)
    requestor = models.CharField(max_length=255, db_column='requestor', blank=True,null=True)
    company_no = models.CharField(max_length=255, db_column='company_no', blank=True,null=True)
    company = models.CharField(max_length=255, db_column='company', blank=True)
    address1 = models.CharField(max_length=255, db_column='address1', blank=True)
    address2 = models.CharField(max_length=255, db_column='address2', blank=True)
    city = models.CharField(max_length=255, db_column='city', blank=True)
    state = models.CharField(max_length=255, db_column='state', blank=True,null=True)
    zip_code = models.CharField(max_length=255, db_column='zip_code', blank=True)
    phone = models.CharField(max_length=255, db_column='phone', blank=True,null=True)
    ext = models.CharField(max_length=255, db_column='ext', blank=True,null=True)
    fax = models.CharField(max_length=255, db_column='fax', blank=True,null=True)
    email = models.CharField(max_length=255, db_column='email', blank=True,null=True)
    tpo = models.CharField(max_length=255, db_column='tpo', blank=True,null=True)
    medicare = models.CharField(max_length=255, db_column='medicare', blank=True,null=True)
    suspend = models.CharField(max_length=255, db_column='suspend', blank=True,null=True)
    empl_open = models.CharField(max_length=255, db_column='empl_open', blank=True,null=True)
    time_opened = models.CharField(max_length=20, db_column='time_opened', blank=True,null=True)
    empl_close = models.CharField(max_length=255, db_column='empl_close', blank=True,null=True)
    close_date = models.CharField(max_length=20, db_column='close_date', blank=True,null=True)
    time_closed = models.CharField(max_length=20, db_column='time_closed', blank=True,null=True)
    cng_open_time = models.CharField(max_length=20, db_column='cng_open_time', blank=True,null=True)
    cng_close_time = models.CharField(max_length=20, db_column='cng_close_time', blank=True,null=True)
    invoice_no = models.CharField(max_length=255, db_column='invoice_no', blank=True)
    balance = models.CharField(max_length=20, db_column='balance', blank=True,null=True)
    paper_copy_pages = models.CharField(max_length=20, db_column='paper_copy_pages', blank=True,null=True)
    other_pages = models.CharField(max_length=20, db_column='other_pages', blank=True,null=True)
    notes = models.TextField(db_column='notes', blank=True,null=True)
    patient_first_name = models.CharField(max_length=100, blank=True,null=True)
    patient_last_name = models.CharField(max_length=100, blank=True,null=True)
    patient_date_of_birth = models.DateField(blank=True,null=True)
    requestor_name = models.CharField(max_length=100, blank=True,null=True)
    requestor_email = models.EmailField(blank=True,null=True)
    request_type = models.CharField(max_length=50, blank=True,null=True)
    request_file = models.FileField(upload_to='requests/', null=True, blank=True)
    patient_no = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    approve_doc_path = models.CharField(max_length=255, db_column='approve_doc_path', blank=True,null=True)
    approve_doc_status = models.CharField(max_length=10, db_column='approve_doc_status', blank=True,null=True)     
    
    ev_createddatetime = models.CharField(db_column='ev_createddatetime', max_length=100, blank=True,
                                            null=True) 
    external_request_createddatetime = models.CharField(db_column='external_request_createddatetime', max_length=100, blank=True,
                                            null=True)  
    
    ev_assigned_createddatetime=models.CharField(db_column='ev_assigned_createddatetime', max_length=100, blank=True,
                                      null=True)
    
    ev_closed_createddatetime=models.CharField(db_column='ev_closed_createddatetime', max_length=100, blank=True,
                                      null=True)
    ev_remarks = models.CharField(db_column='ev_remarks', max_length=100, blank=True,
                                      null=True)
    ev_status = models.CharField(db_column='ev_status', max_length=100, blank=True,
                                      null=True, default='New')
    ev_assigned_to = models.CharField(db_column='ev_assigned_to', max_length=255, blank=True, null=True)
    ev_assigned_name = models.CharField(db_column='ev_assigned_name', max_length=100, blank=True,null=True)
    misc1_path = models.TextField(blank=True, default='')
    misc2_path = models.TextField(blank=True, default='')
    misc3_path = models.TextField(blank=True, default='')
    misc4_path = models.TextField(blank=True, default='')
    misc5_path = models.TextField(blank=True, default='')
    misc6_path = models.TextField(blank=True, default='')
    misc7_path = models.TextField(blank=True, default='')
    misc8_path = models.TextField(blank=True, default='')
    misc9_path = models.TextField(blank=True, default='')
    misc10_path = models.TextField(blank=True, default='')

    file_path = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)



    misc1_pages = models.IntegerField(default=0)
    misc2_pages = models.IntegerField(default=0)
    misc3_pages = models.IntegerField(default=0)
    misc4_pages = models.IntegerField(default=0)
    misc5_pages = models.IntegerField(default=0)
    misc6_pages = models.IntegerField(default=0)
    misc7_pages = models.IntegerField(default=0)
    misc8_pages = models.IntegerField(default=0)
    misc9_pages = models.IntegerField(default=0)
    misc10_pages = models.IntegerField(default=0)




    total_pages = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    invoice_pdf_path = models.TextField(null=True, blank=True)

    patient_from_date = models.DateField(blank=True,null=True)
    patient_to_date = models.DateField(blank=True,null=True)

    file_from_date = models.DateField(blank=True,null=True)
    file_to_date = models.DateField(blank=True,null=True)

    

    misc1_start_date = models.DateField(blank=True, null=True)
    misc1_end_date = models.DateField(blank=True, null=True)

    misc2_start_date = models.DateField(blank=True, null=True)
    misc2_end_date = models.DateField(blank=True, null=True)

    misc3_start_date = models.DateField(blank=True, null=True)
    misc3_end_date = models.DateField(blank=True, null=True)

    misc4_start_date = models.DateField(blank=True, null=True)
    misc4_end_date = models.DateField(blank=True, null=True)

    misc5_start_date = models.DateField(blank=True, null=True)
    misc5_end_date = models.DateField(blank=True, null=True)

    misc6_start_date = models.DateField(blank=True, null=True)
    misc6_end_date = models.DateField(blank=True, null=True)

    misc7_start_date = models.DateField(blank=True, null=True)
    misc7_end_date = models.DateField(blank=True, null=True)

    misc8_start_date = models.DateField(blank=True, null=True)
    misc8_end_date = models.DateField(blank=True, null=True)

    misc9_start_date = models.DateField(blank=True, null=True)
    misc9_end_date = models.DateField(blank=True, null=True)

    misc10_start_date = models.DateField(blank=True, null=True)
    misc10_end_date = models.DateField(blank=True, null=True)

    

    
    class Meta:
        db_table = 'upstremform'




class ChargingList(models.Model):
    state = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    base_fare = models.CharField(max_length=255, blank=True, null=True)
    minimum_fee = models.CharField(max_length=255, blank=True, null=True)
    flat_fee = models.CharField(max_length=255, blank=True, null=True)
    free_for = models.CharField(max_length=255, blank=True, null=True)
    per_page = models.CharField(max_length=255, blank=True, null=True)
    fee_limit = models.CharField(max_length=255, blank=True, null=True)
    fee_limit_for_mail = models.CharField(max_length=255, blank=True, null=True)
    fee_limit_for_electronic = models.CharField(max_length=255, blank=True, null=True)
    page_1 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_5 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_10 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_20 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_25 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_30 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_40 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_50 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_80 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_100 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_150 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_250 = models.CharField(max_length=255, blank=True, null=True)
    page_1_to_1000 = models.CharField(max_length=255, blank=True, null=True)
    page_2_to_30 = models.CharField(max_length=255, blank=True, null=True)
    page_2_to_200 = models.CharField(max_length=255, blank=True, null=True)
    page_11_to_20 = models.CharField(max_length=255, blank=True, null=True)
    page_11_to_40 = models.CharField(max_length=255, blank=True, null=True)
    page_11_to_50 = models.CharField(max_length=255, blank=True, null=True)
    page_21_to_30 = models.CharField(max_length=255, blank=True, null=True)
    page_21_to_40 = models.CharField(max_length=255, blank=True, null=True)
    page_21_to_50 = models.CharField(max_length=255, blank=True, null=True)
    page_21_to_60 = models.CharField(max_length=255, blank=True, null=True)
    page_21_to_100 = models.CharField(max_length=255, blank=True, null=True)
    page_21_to_500 = models.CharField(max_length=255, blank=True, null=True)
    page_26_to_100 = models.CharField(max_length=255, blank=True, null=True)
    page_26_to_350 = models.CharField(max_length=255, blank=True, null=True)
    page_31_to_100 = models.CharField(max_length=255, blank=True, null=True)
    page_101_to_200 = models.CharField(max_length=255, blank=True, null=True)
    above_5_pages = models.CharField(max_length=255, blank=True, null=True)
    above_10_pages = models.CharField(max_length=255, blank=True, null=True)
    above_20_pages = models.CharField(max_length=255, blank=True, null=True)
    above_25_pages = models.CharField(max_length=255, blank=True, null=True)
    above_30_pages = models.CharField(max_length=255, blank=True, null=True)
    above_40_pages = models.CharField(max_length=255, blank=True, null=True)
    above_50_pages = models.CharField(max_length=255, blank=True, null=True)
    above_60_pages = models.CharField(max_length=255, blank=True, null=True)
    above_80_pages = models.CharField(max_length=255, blank=True, null=True)
    above_100_pages = models.CharField(max_length=255, blank=True, null=True)
    above_150_pages = models.CharField(max_length=255, blank=True, null=True)
    above_200_pages = models.CharField(max_length=255, blank=True, null=True)
    above_250_pages = models.CharField(max_length=255, blank=True, null=True)
    above_350_pages = models.CharField(max_length=255, blank=True, null=True)
    above_500_pages = models.CharField(max_length=255, blank=True, null=True)
    above_1000_pages = models.CharField(max_length=255, blank=True, null=True)
    first_hour = models.CharField(max_length=255, blank=True, null=True)
    each_additional_hour = models.CharField(max_length=255, blank=True, null=True)
    required_fee = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    optional_fee = models.CharField(max_length=255, blank=True, null=True)
    amount_1 = models.CharField(max_length=255, blank=True, null=True)
    optional_fee_1 = models.CharField(max_length=255, blank=True, null=True)
    amount_2 = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mail = models.CharField(max_length=255, blank=True, null=True)



    class Meta:
        db_table = 'charging_list'
