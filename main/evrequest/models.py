from django.db import models

# Create your models here.

 

class EvDetails(models.Model): 
    ev_remarks = models.CharField(db_column='ev_remarks', max_length=50, blank=True,
                                      null=True)
    ev_status = models.CharField(db_column='ev_status', max_length=50, blank=True,
                                      null=True)
    ev_assigned_to = models.CharField(db_column='ev_assigned_to', max_length=10, blank=True,null=True)
    ev_assigned_name = models.CharField(db_column='ev_assigned_name', max_length=100, blank=True,null=True)
    Date_of_service = models.CharField(db_column='Date_of_service', max_length=50, blank=True,null=True)
    patient_name = models.CharField(db_column='patient_name', max_length=200, blank=True,null=True)
    patient_id = models.CharField(db_column='patient_id', max_length=100, blank=True,null=True)
    patient_dob = models.CharField(db_column='patient_dob', max_length=50, blank=True,null=True)
    plan_network = models.CharField(db_column='plan_network', max_length=200, blank=True,null=True)
    subscriber_id = models.CharField(db_column='subscriber_id', max_length=100, blank=True,null=True) 
    subscriber_name	 = models.CharField(db_column='subscriber_name', max_length=250, blank=True,null=True)
    subscriber_dob	 = models.CharField(db_column='subscriber_dob', max_length=50, blank=True,null=True)
   
    ev_createddatetime = models.CharField(db_column='ev_createddatetime', max_length=100, blank=True,
                                            null=True)  # Field name made lowercase.
    
    ev_assigned_createddatetime=models.CharField(db_column='ev_assigned_createddatetime', max_length=100, blank=True,
                                      null=True)
    
    ev_closed_createddatetime=models.CharField(db_column='ev_closed_createddatetime', max_length=100, blank=True,
                                      null=True)
    ev_review_created_datetime=models.CharField(db_column='ev_review_created_datetime', max_length=100, blank=True,
                                      null=True)
    ev_assigned_timedifference=models.CharField(db_column='ev_assigned_timedifference', max_length=50, blank=True,
                                      null=True)
    ev_progress_timedifference=models.CharField(db_column='ev_progress_timedifference', max_length=50, blank=True,
                                      null=True)
    ev_id = models.AutoField(db_column='ev_id', primary_key=True)  # Field name made lowercase.

    def __str__(self):
        return self.title


