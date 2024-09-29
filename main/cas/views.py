from django.shortcuts import render
from django.http import HttpResponse
from .models import CasForm

from register.models import UserDetails
from django.views.decorators.csrf import csrf_exempt


  
def update_userassign_status(userid,flagval):                
    userassigndata=UserDetails.objects.filter(user_id=userid).get()
    assignusername=userassigndata.user_username
    assignid=userassigndata.user_id
    userassigndata.user_assign_flag=flagval
    userassigndata.save()
    return assignusername,assignid

@csrf_exempt  
def insert_casform(request):
    if request.method == 'GET':
        # Retrieve data from the form
        claim_id = request.GET.get('Claim_Number')
        insurance = request.GET.get('Insurance')
        facility = request.GET.get('Facility')
        charge_from_date = request.GET.get('Charge_From_Date')
        charge_to_date = request.GET.get('Charge_To_Date')
        facility_npi = request.GET.get('Facility_NPI')
        primary_member_id = request.GET.get('Primary_Member_ID')
        charge_debit_amount = request.GET.get('Charge_Debit_Amount')
        pat_primary_payer_name = request.GET.get('Pat_Primary_Payer_Name')
        patient_full_name = request.GET.get('Patient_Full_Name')
        patient_birthday = request.GET.get('Patient_Birthday')
        current_billing_status = request.GET.get('Current_Billing_Status')
        claim_number = request.GET.get('Claim_Number')
        patient_account_number = request.GET.get('Patient_Account_Number')
        uhc_availity_claimstatus = request.GET.get('UHC_Availity_ClaimStatus')
        total_billedamount = request.GET.get('Total_BilledAmount')
        total_paid = request.GET.get('Total_Paid')
        total_adjustment = request.GET.get('Total_Adjustment')
        total_patient_responsibility = request.GET.get('Total_Patient_Responsibility')
        service_code = request.GET.get('Service_Code')
        billing_amount = request.GET.get('Billing_Amount')
        allowed_amount = request.GET.get('Allowed_Amount')
        paid_amount = request.GET.get('Paid_Amount')
        check_number = request.GET.get('Check_Number')
        check_date = request.GET.get('Check_Date')
        remark_code = request.GET.get('Remark_Code')
        category_1 = request.GET.get('Category_1')
        status_1 = request.GET.get('Status_1')
        description_1 = request.GET.get('Description_1')
        status_description_1 = request.GET.get('Status_Description_1')
        claim_reason_code_1 = request.GET.get('Claim_Reason_Code_1')
        category_2 = request.GET.get('Category_2')
        status_2 = request.GET.get('Status_2')
        description_2 = request.GET.get('Description_2')
        status_description_2 = request.GET.get('Status_Description_2')
        claim_reason_code_2 = request.GET.get('Claim_Reason_Code_2')
        category_3 = request.GET.get('Category_3')
        status_3 = request.GET.get('Status_3')
        description_3 = request.GET.get('Description_3')
        status_description_3 = request.GET.get('Status_Description_3')
        bot_status = request.GET.get('Bot_Status')
        comments = request.GET.get('Comments')
        updated_by = request.GET.get('Updated_By')
        rcm_comments = request.GET.get('RCM_Comments')

        
        userdata=UserDetails.objects.filter(user_checklist='1').order_by('user_id')
        row_exists = userdata.exists()
        if row_exists:
            useridlist=[]
            userflaglist=[]
            for users in userdata:
                useridlist.append(users.user_id)
                userflaglist.append(users.user_assign_flag)

            if '1' not in userflaglist:
                userid=useridlist[0]
                assignusername , assignid = update_userassign_status(userid,1)
            else:
                index = userflaglist.index('1')
                indexplus=index+1
                try:
                    olduserid=useridlist[index]
                    assignusername , assignid = update_userassign_status(olduserid,0)
                    userid=useridlist[indexplus]
                    assignusername , assignid = update_userassign_status(userid,1)
                except:
                    userid=useridlist[0]
                    assignusername , assignid = update_userassign_status(userid,1)
            evstatus="In-progress"

        else:
            evstatus="New"
            assignusername , assignid = '' , ''
        
        # # Create a new CasForm object and save it to the database
        cas_form = CasForm(
            Claim_ID=claim_id,
            Insurance=insurance,
            Facility=facility,
            Charge_From_Date=charge_from_date,
            Charge_To_Date=charge_to_date,
            Facility_NPI=facility_npi,
            Primary_Member_ID=primary_member_id,
            Charge_Debit_Amount=charge_debit_amount,
            Pat_Primary_Payer_Name=pat_primary_payer_name,
            Patient_Full_Name=patient_full_name,
            Patient_Birthday=patient_birthday,
            Current_Billing_Status=current_billing_status,
            Claim_Number=claim_number,
            Patient_Account_Number=patient_account_number,
            UHC_Availity_ClaimStatus=uhc_availity_claimstatus,
            Total_BilledAmount=total_billedamount,
            Total_Paid=total_paid,
            Total_Adjustment=total_adjustment,
            Total_Patient_Responsibility=total_patient_responsibility,
            Service_Code=service_code,
            Billing_Amount=billing_amount,
            Allowed_Amount=allowed_amount,
            Paid_Amount=paid_amount,
            Check_Number=check_number,
            Check_Date=check_date,
            Remark_Code=remark_code,
            Category_1=category_1,
            Status_1=status_1,
            Description_1=description_1,
            Status_Description_1=status_description_1,
            Claim_Reason_Code_1=claim_reason_code_1,
            Category_2=category_2,
            Status_2=status_2,
            Description_2=description_2,
            Status_Description_2=status_description_2,
            Claim_Reason_Code_2=claim_reason_code_2,
            Category_3=category_3,
            Status_3=status_3,
            Description_3=description_3,
            Status_Description_3=status_description_3,
            Bot_Status=bot_status,
            Comments=comments,
            Updated_By=updated_by,
            RCM_Comments=rcm_comments,
            cas_assigned_name=assignusername,
            cas_status=evstatus,
            cas_assigned_to=assignid
        )
        cas_form.save()
        
        # Redirect to a success page or render a success message
        return HttpResponse("Record inserted successfully!")
    else:
        # If not a GET request, render the form page
        return HttpResponse("Record not inserted")
