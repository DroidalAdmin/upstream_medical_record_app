from django.contrib import messages
from django.db import connection
from django.http import HttpResponse, response, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from datetime import datetime, timedelta
from .models import EvDetails
from cas.models import CasForm
from register.models import UserDetails
from upstreamform.models import UpstreamForm
from plotly.offline import plot
from plotly.graph_objs import Scatter
from datetime import datetime
from django.core.mail import send_mail 
from django.template.loader import render_to_string
import os 
import json
from django.contrib.auth.decorators import login_required
import pandas as pd
from collections import defaultdict
import plotly.graph_objects as go
from plotly.offline import plot

# Create your views here.


def send_email_view(sub,mailtype,toaddr,userName,evid):
    subject = sub
    message = sub
    from_email = 'iverify@droidal.com' #filemanager@droidal.com
    recipient_list = [toaddr]
    if mailtype=="new":
        template_path = 'requestevmail.html'  # Update this path to the actual path of your template
    else:
        template_path = 'assignemail.html'  # Update this path to the actual path of your template
    context = {
        'username': userName,  
        'recordid':evid
    }

    # Render the HTML content of the email
    email_html = render_to_string(template_path, context)

    send_mail(subject, message, from_email, recipient_list,html_message=email_html)



def calculate_time_difference(from_datetime_str, to_datetime_str):
    # Convert string representations to datetime objects
    from_datetime = datetime.strptime(from_datetime_str, '%Y-%m-%d %H:%M:%S')
    to_datetime = datetime.strptime(to_datetime_str, '%Y-%m-%d %H:%M:%S')

    # Calculate the time difference
    time_difference = to_datetime - from_datetime

    # Extract hours, minutes, and seconds from the time difference
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format the result as HH:MM:SS
    time_difference_formatted = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

    return time_difference_formatted


def analytics(request):
    try:
        if request.method == 'GET':
            
            labels = ['In-progress', 'Completed', 'Error']
            values = [25, 30, 20]
            colors = ['darkblue', 'cyan', 'royalblue']

            print(f"Labels: {labels}, Values: {values}, Colors: {colors}")

            fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors), pull=[0.1, 0, 0])])

            print(f"Figure created: {fig}")

            fig.update_layout(
                margin=dict(l=0, r=0, b=0, t=50),  # Adjust margin for better presentation
                legend=dict(title='', orientation='h', y=1, yanchor='bottom', x=0.5, xanchor='center'),
            )

            print("Layout updated for the figure")

            plt_div = plot(fig, output_type='div')

            print(f"Plot Div: {plt_div[:100]}...")  

            context = {'plot_div': plt_div}

            # print(f"Context: {context}")

            return render(request, 'analytics.html', context)
        
        else:
            print("Received a non-GET request")
            return render(request, 'analytics.html')

    except Exception as e:
        print(f"An error occurred in analytics view: {e}", exc_info=True)
        return render(request, 'error.html', {'error': str(e)})
   
   
def userlist(request):
    userdata=UserDetails.objects.filter(user_Type='rcm').order_by('user_id')
    context = {'users':userdata}
    return render(request,'userlist.html',context)


@csrf_exempt   
def userchecklist(request):
    if request.method == 'POST':
        userid=request.POST['userid']
        flag_value=request.POST['flag_value']
        userdata = UserDetails.objects.get(user_id=userid)
        userdata.user_checklist=flag_value
        userdata.save()
        return HttpResponse('Success')
    
 

@csrf_exempt
def editreg(request, id):
    if request.method == 'GET':
        data = EvDetails.objects.get(ev_id=id) 
        context = {'datas': data}
        return render(request,'edit.html',context)
    elif request.method == 'POST':
        form = request.POST 
        updatedata = EvDetails.objects.get(ev_id=id)  
        updatedata.Date_of_service=form['date_of_service']
        updatedata.patient_name=form['patient_name']
        updatedata.patient_id=form['patient_id']
        updatedata.patient_dob=form['patient_dob']
        updatedata.plan_network=form['plan_network']
        updatedata.subscriber_id=form['subscriber_id']
        updatedata.subscriber_name=form['subscriber_name']
        updatedata.subscriber_dob=form['subscriber_dob']
        updatedata.save()
        return HttpResponseRedirect('/upstream/registration/')
    
def deletecas(request,id):
    if request.method == 'GET':
        data = CasForm.objects.get(casid=id)
        data.delete()
        return redirect('/upstream/registration/')


def deletereg(request, id):
    if request.method == 'GET':
        data = EvDetails.objects.get(ev_id=id)
        data.delete()
        return redirect('/upstream/registration/')
    
def statusupdatereg(request):
    if request.method == 'GET':
        form = request.GET
        id=form['remarkid']
        updatedata = EvDetails.objects.get(ev_id=id) 
        assigneddate=updatedata.ev_assigned_createddatetime
        now=datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')  
        updatedata.ev_status=form['status']
        updatedata.ev_remarks=form['remarks']
        if form['status']!="In-Review":
            updatedata.ev_closed_createddatetime=formatted_date   
        else:
            updatedata.ev_review_created_datetime=formatted_date   
        timediff=calculate_time_difference(assigneddate,formatted_date)
        if form['status']!="In-progress":
            updatedata.ev_progress_timedifference=timediff
        updatedata.save()
        return HttpResponseRedirect('/upstream/registration/')
    
def completereg(request,id):
   if request.method == 'GET':
      updatedata = EvDetails.objects.get(ev_id=id) 
      updatedata.ev_status="Completed"
      updatedata.save()
      return HttpResponseRedirect('/upstream/registration/')
   
def errorreg(request,id):
   if request.method == 'GET':
      updatedata = EvDetails.objects.get(ev_id=id) 
      updatedata.ev_status="Error"
      updatedata.save()
      return HttpResponseRedirect('/upstream/registration/')
   
def inprogressreg(request,id):
   if request.method == 'GET':
      updatedata = EvDetails.objects.get(ev_id=id) 
      updatedata.ev_status="In-progress"
      updatedata.save()
      return HttpResponseRedirect('/upstream/registration/')
   

@csrf_exempt
def evrequestpage(request):
    if request.method == 'GET':
        return render(request, 'ev_form.html') 
    
    elif request.method == 'POST':
        form = request.POST 
        now=datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')  

        newentry = EvDetails.objects.create(Date_of_service=form['date_of_service'],
                                            patient_name=form['patient_name'],
                                            patient_id=form['patient_id'],
                                            patient_dob=form['patient_dob'],
                                            plan_network=form['plan_network'],
                                            subscriber_id=form['subscriber_id'],
                                            subscriber_name=form['subscriber_name'],
                                            subscriber_dob=form['subscriber_dob'],
                                            ev_status='New',
                                            ev_createddatetime=formatted_date,
                                        )
        if newentry:
           send_email_view('New Record Assigned','new','iverify@droidal.com','Admin',newentry.ev_id) 
           return HttpResponseRedirect('/upstream/registration/')
        else:
           return render(request, 'ev_form.html')

  
def update_userassign_status(userid,flagval):                
    userassigndata=UserDetails.objects.filter(user_id=userid).get()
    assignusername=userassigndata.user_username
    assignid=userassigndata.user_id
    userassigndata.user_assign_flag=flagval
    userassigndata.save()
    return assignusername,assignid

@csrf_exempt
def evregister(request):
    form = request.GET    
    now=datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')  

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

    newentry = EvDetails.objects.create(Date_of_service=form['date_of_service'],
                                        patient_name=form['patient_name'],
                                        patient_id=form['patient_id'],
                                        patient_dob=form['patient_dob'],
                                        plan_network=form['plan_network'],
                                        subscriber_id=form['subscriber_id'],
                                        subscriber_name=form['subscriber_name'],
                                        subscriber_dob=form['subscriber_dob'],                                        
                                        ev_status=evstatus,
                                        ev_assigned_to=assignid,
                                        ev_assigned_name=assignusername,
                                        ev_createddatetime=formatted_date,
                                    ) 

    if newentry:
        send_email_view('New Record Assigned','new','iverify@droidal.com','Admin',newentry.ev_id) 
        return JsonResponse({"message":"Record added successfully."})
    else:
        return JsonResponse({"message":"Please Try once again."})


@csrf_exempt
def assignuser(request,id,aid):
    if request.method == "GET":       
        updatedata = EvDetails.objects.get(ev_id=id) 
        ev_createddate=updatedata.ev_createddatetime
        updatedata.ev_assigned_to=aid 
        userdata=UserDetails.objects.all()
        assigned_username = None
        now=datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')  
        for users in userdata:
            if aid == users.user_id:
                asingedusername=users.user_username
                asingedemail=users.user_email
        updatedata.ev_assigned_name=asingedusername
        updatedata.ev_status="In-progress"
        updatedata.ev_assigned_createddatetime=formatted_date
        timediff=calculate_time_difference(ev_createddate,formatted_date)
        updatedata.ev_assigned_timedifference=timediff
        updatedata.save()
        send_email_view('New Record Assigned','assigned',asingedemail,asingedusername,id)
        return HttpResponseRedirect('/upstream/registration/')
    

def excel_to_dict(file_path):
    # Read the Excel file into a pandas DataFrame
    excel_data = pd.read_excel(file_path)

    # Convert the DataFrame to a list of dictionaries
    excel_dict_list = excel_data.to_dict(orient='records')

    return excel_dict_list


@csrf_exempt
def updatefilerecord(request):  
    if request.method == 'POST' and request.FILES['form_upload']:
        uploaded_file = request.FILES['form_upload']
        
        # Define the path where you want to save the file inside the 'static' folder
        static_folder = 'static/uploads'
        file_path = os.path.join(static_folder, uploaded_file.name)
        
        now=datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S') 

        # Save the file
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        
        mydict=excel_to_dict(file_path)

        for datas in mydict: 
            newentry = EvDetails.objects.create( 
                                           Date_of_service=datas['Date of service'],
                                           patient_name=datas['Patient Name'],
                                           patient_id=datas['Patient ID'],
                                           patient_dob=datas['Patient DOB'], 
                                           subscriber_dob=datas['Subscriber DOB'],
                                           subscriber_name=datas['Subscriber Name'], 
                                           subscriber_id=datas['Subscriber ID/SSN'], 
                                           plan_network=datas['Plan/Network'],
                                           ev_status='New',
                                           ev_createddatetime=formatted_date,
                                        )


        return HttpResponseRedirect('/upstream/registration/')


@csrf_exempt   
def date_range_view(request):
    return HttpResponseRedirect('/upstream/welcome/')
    # from_date = request.GET.get('fromdate')
    # to_date = request.GET.get('todate')

    
    # if(request.session['usertype']=='rcm'):
    #     userids=request.session['uid']
    #     if from_date=="":
    #        overalldata = EvDetails.objects.filter(ev_assigned_to=userids)
    #     else:
    #        overalldata = EvDetails.objects.filter(ev_assigned_to=userids,ev_appointdate=[from_date,to_date])
    # else:
    #     if from_date=="":
    #         overalldata = EvDetails.objects.order_by('-ev_appointdate')
    #     else:
    #        overalldata = EvDetails.objects.filter(ev_appointdate=[from_date,to_date])
           
    # import plotly.graph_objects as go

    # # Sample data
    # labels = ['In-progress', 'Completed', 'Error']
    # values = [25, 30, 20]
    # colors = ['darkblue', 'cyan', 'royalblue']

    # # Create a 3D Pie chart
    # fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors),pull=[0.1, 0, 0, 0])])
    
    # fig.update_layout(
    #     margin=dict(l=0, r=0, b=0, t=50),  # Adjust margin for better presentation
    #     legend=dict(title='', orientation='h', y=1, yanchor='bottom', x=0.5, xanchor='center'),
    # ) 

    # plt_div = plot(fig, output_type='div')
    # context = {'datas': overalldata, 'plot_div': plt_div}
    # return render(request,'welcome.html',context) 
     
 
@csrf_exempt
def Create(request):
  if request.method == 'GET':
    return render(request, 'ev_form.html')

  elif request.method == 'POST':
    form = request.POST
    email = form['email']
    firstname = form['firstname']
    lastname = form['lastname'] 
    mobilenumber = form['mobilenumber']
    organization = form['organization']
    designation = form['designation']
    user = form['user']
    password = form['password']

    userdet = EvDetails.objects.create(user_email=email,user_firstname=firstname,user_lastname=lastname,user_mobile=mobilenumber,user_company=organization,user_designation=designation,user_username=user,user_password=password)
    if userdet:

        return HttpResponseRedirect('/upstream/welcome/')
    else:
        return render(request, 'ev_form.html')
    



@csrf_exempt
def daterange_view(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        from_date = body.get('fromdate')
        to_date = body.get('todate')

        if not from_date or not to_date:
            # Calculate default date range: last 4 months
            to_date = datetime.now()
            from_date = to_date - timedelta(days=120)  # Roughly 4 months
            from_date = from_date.strftime('%Y-%m-%d')
            to_date = to_date.strftime('%Y-%m-%d')

        # Determine user role
        username = request.session.get('username')
        usertype = request.session.get('usertype')
        user_id = request.session.get('uid')
        
        # Fetch data from the database based on role
        if usertype == 'admin':
            ev_requests = UpstreamForm.objects.filter(ev_createddatetime__range=[from_date, to_date]).values('ev_createddatetime')
            external_requests = UpstreamForm.objects.filter(external_request_createddatetime__range=[from_date, to_date]).values('external_request_createddatetime')
            assigned_requests = UpstreamForm.objects.filter(ev_assigned_createddatetime__range=[from_date, to_date]).values('ev_assigned_createddatetime')
            completed_requests = UpstreamForm.objects.filter(ev_closed_createddatetime__range=[from_date, to_date]).values('ev_closed_createddatetime')
        elif usertype == 'Internal-user':
            user_details = UserDetails.objects.get(user_id=user_id)
            full_name = f"{user_details.user_firstname} {user_details.user_lastname}"
            
            ev_requests = UpstreamForm.objects.filter(ev_createddatetime__range=[from_date, to_date]).values('ev_createddatetime')
            external_requests = UpstreamForm.objects.filter(external_request_createddatetime__range=[from_date, to_date]).values('external_request_createddatetime')
            assigned_requests = UpstreamForm.objects.filter(ev_assigned_to=full_name, ev_assigned_createddatetime__range=[from_date, to_date]).values('ev_assigned_createddatetime')
            completed_requests = UpstreamForm.objects.filter(ev_assigned_to=full_name, ev_closed_createddatetime__range=[from_date, to_date]).values('ev_closed_createddatetime')
        else:
            ev_requests = []
            external_requests = []
            assigned_requests = []
            completed_requests = []

        # Initialize counters
        ev_requests_count = defaultdict(int)
        external_requests_count = defaultdict(int)
        assigned_requests_count = defaultdict(int)
        completed_requests_count = defaultdict(int)

        # Function to parse date and count by month
        def count_by_month(data, counter, date_field):
            for item in data:
                date_str = item[date_field]
                if date_str:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')  # Adjust format as needed
                    month = date_obj.strftime('%b %y')  # Format as "Mon YY"
                    counter[month] += 1

        # Count ev requests by month
        count_by_month(ev_requests, ev_requests_count, 'ev_createddatetime')
        # Count external requests by month
        count_by_month(external_requests, external_requests_count, 'external_request_createddatetime')
        # Count assigned requests by month
        count_by_month(assigned_requests, assigned_requests_count, 'ev_assigned_createddatetime')
        # Count completed requests by month
        count_by_month(completed_requests, completed_requests_count, 'ev_closed_createddatetime')

        # Calculate total new requests by summing ev requests and external requests
        total_new_requests_count = defaultdict(int)
        for month in set(ev_requests_count.keys()).union(external_requests_count.keys()):
            total_new_requests_count[month] = ev_requests_count[month] + external_requests_count[month]

        # Convert to list of counts sorted by actual date order and then reverse the months
        sorted_months = sorted(total_new_requests_count.keys(), key=lambda x: datetime.strptime(x, '%b %y'))[::-1]
        total_new_requests_list = [total_new_requests_count[month] for month in sorted_months]
        assigned_requests_list = [assigned_requests_count[month] for month in sorted_months]
        completed_requests_list = [completed_requests_count[month] for month in sorted_months]

        data = {
            'new_requests': total_new_requests_list,
            'assigned_requests': assigned_requests_list,
            'completed_requests': completed_requests_list,
            'months': sorted_months
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
