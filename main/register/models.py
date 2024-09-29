from django.db import models

# Create your models here.

class UserDetails(models.Model):
    user_firstname = models.CharField(db_column='user_Firstname', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    user_lastname = models.CharField(db_column='user_Lastname', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    user_mobile = models.CharField(db_column='user_Mobile', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    user_email = models.CharField(db_column='user_Email', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.
    user_designation = models.CharField(db_column='user_Designation', max_length=100, blank=True,
                                        null=True)  # Field name made lowercase.
    user_company = models.CharField(db_column='user_Company', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase. 
    user_SecretKey = models.CharField(db_column='user_SecretKey', max_length=255, blank=True,
                                    null=True) 
    user_checklist= models.CharField(db_column='user_Checklist', max_length=20, blank=True,
                                    null=True) 
    user_assign_flag= models.CharField(db_column='user_assign_flag', max_length=10, blank=True,
                                    null=True) 
    user_username = models.TextField(db_column='user_Username', blank=True, null=True)  # Field name made lowercase.
    user_password = models.TextField(db_column='user_Password', blank=True, null=True)  # Field name made lowercase.
    user_createddatetime = models.DateField(db_column='user_Createddatetime', blank=True,
                                            null=True)  # Field name made lowercase.
    user_Type = models.CharField(db_column='user_Type',max_length=50,blank=True,null=True)
    user_id = models.AutoField(db_column='user_ID', primary_key=True)  # Field name made lowercase.



    class Meta:
        db_table = 'register_userdetails'
 

