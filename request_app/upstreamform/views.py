from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse, response, HttpResponseRedirect, Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UpstreamForm, ChargingList, RequestFile 
from datetime import datetime
from django.core.mail import EmailMessage

from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
import PyPDF2
from PyPDF2 import *
import time 
import requests
import pdfkit
from django.utils import timezone
import json
import logging
from urllib.parse import quote, unquote
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
import pandas as pd
import zipfile
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

# def clean_dollar_value(value):
#     """
#     This function strips the '$' symbol and converts the remaining string to a float.
#     If the value is NaN or empty, it returns None.
#     """
#     if pd.notna(value) and isinstance(value, str) and '$' in value:
#         return float(value.replace('$', '').replace(',', '').strip())
#     elif pd.notna(value):
#         return value
#     else:
#         return None

# def import_data_view(request):
#     if request.method == "POST":
#         file_path = r'C:\Users\abdulwahid.j\Downloads\Charging list 2 - Copy(Sheet1).csv'
#         df = pd.read_csv(file_path)

#         for index, row in df.iterrows():
#             charging_list_entry = ChargingList(
#                 state=row['state'] if pd.notna(row['state']) else None,
#                 category=row['Category'] if pd.notna(row['Category']) else None,
#                 base_fare=clean_dollar_value(row['Base Fare']),
#                 flat_fee=clean_dollar_value(row['Flat Fee']),
#                 free_for=row['Free For'] if pd.notna(row['Free For']) else None,
#                 per_page=clean_dollar_value(row['Per Page']),
#                 fee_limit=clean_dollar_value(row['Fee Limit']),
#                 page_1=clean_dollar_value(row['1 page']),
#                 page_1_to_5=clean_dollar_value(row['1 to 5 pages']),
#                 page_1_to_10=clean_dollar_value(row['1 to 10 pages']),
#                 page_1_to_20=clean_dollar_value(row['1 to 20 pages']),
#                 page_1_to_25=clean_dollar_value(row['1 to 25 pages']),
#                 page_1_to_30=clean_dollar_value(row['1 to 30 pages']),
#                 page_1_to_40=clean_dollar_value(row['1 to 40 pages']),
#                 page_1_to_50=clean_dollar_value(row['1 to 50 pages']),
#                 page_1_to_80=clean_dollar_value(row['1 to 80 pages']),
#                 page_1_to_100=clean_dollar_value(row['1 to 100 pages']),
#                 page_1_to_150=clean_dollar_value(row['1 to 150 pages']),
#                 page_1_to_250=clean_dollar_value(row['1 to 250 pages']),
#                 page_1_to_1000=clean_dollar_value(row['1 to 1000 pages']),
#                 page_2_to_30=clean_dollar_value(row['2 to 30 pages']),
#                 page_2_to_200=clean_dollar_value(row['2 to 200']),
#                 page_11_to_20=clean_dollar_value(row['11 to 20 pages']),
#                 page_11_to_40=clean_dollar_value(row['11 to 40 pages']),
#                 page_11_to_50=clean_dollar_value(row['11 to 50 pages']),
#                 page_21_to_30=clean_dollar_value(row['21 to 30 pages']),
#                 page_21_to_40=clean_dollar_value(row['21 to 40 pages']),
#                 page_21_to_50=clean_dollar_value(row['21 to 50 pages']),
#                 page_21_to_60=clean_dollar_value(row['21 to 60 pages']),
#                 page_21_to_100=clean_dollar_value(row['21 to 100 pages']),
#                 page_21_to_500=clean_dollar_value(row['21 to 500 pages']),
#                 page_26_to_100=clean_dollar_value(row['26 to 100 pages']),
#                 page_26_to_350=clean_dollar_value(row['26 to 350 pages']),
#                 page_31_to_100=clean_dollar_value(row['31 to 100 pages']),
#                 page_101_to_200=clean_dollar_value(row['101 to 200 pages']),
#                 above_5_pages=clean_dollar_value(row['Above 5 pages']),
#                 above_10_pages=clean_dollar_value(row['Above 10 pages']),
#                 above_20_pages=clean_dollar_value(row['Above 20 pages']),
#                 above_25_pages=clean_dollar_value(row['Above 25 pages']),
#                 above_30_pages=clean_dollar_value(row['Above 30 pages']),
#                 above_40_pages=clean_dollar_value(row['Above 40 pages']),
#                 above_50_pages=clean_dollar_value(row['Above 50 pages']),
#                 above_60_pages=clean_dollar_value(row['Above 60 pages']),
#                 above_80_pages=clean_dollar_value(row['Above 80 pages']),
#                 above_100_pages=clean_dollar_value(row['Above 100 pages']),
#                 above_150_pages=clean_dollar_value(row['Above 150 pages']),
#                 above_200_pages=clean_dollar_value(row['Above 200 pages']),
#                 above_250_pages=clean_dollar_value(row['Above 250 pages']),
#                 above_350_pages=clean_dollar_value(row['Above 350 pages']),
#                 above_500_pages=clean_dollar_value(row['Above 500 pages']),
#                 above_1000_pages=clean_dollar_value(row['Above 1000 pages']),
#                 required_fee=clean_dollar_value(row['Required fee']),
#                 amount=clean_dollar_value(row['Amount']),
#                 optional_fee=clean_dollar_value(row['Optional fee']),
#                 amount_1=clean_dollar_value(row['Amount.1']),
#                 optional_fee_1=clean_dollar_value(row['Optional fee.1']),
#                 amount_2=clean_dollar_value(row['Amount.2']),
#             )
#             charging_list_entry.save()

#         return JsonResponse({"status": "success", "message": "Data imported successfully."})
#     else:
#         return JsonResponse({"status": "fail", "message": "Invalid request method."})

@csrf_exempt 
def updateauthapprove(request):
    if request.method == 'POST':
        flag_id = request.POST.get('flag_id') 
        flag_value = request.POST.get('flag_value')
        updatedata = UpstreamForm.objects.get(request_id=int(flag_id))  
        updatedata.approve_doc_status =  flag_value
        updatedata.save()
        return HttpResponse('Status Updated Successfully...')


def htmlbootstraplink():
    return '''
    <style>
    body {
        font-family: Arial, sans-serif;
    }
    .header-title {
        font-size: 24px;
        font-weight: bold;
    }
    .form-group {
        margin-bottom: 15px;
    }
    .form-control {
        width: 100%;
        padding: 8px;
    }
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
    .pull-left {
        float: left;
    }
    .pull-right {
        float: right;
    }
    .m-t-30 {
        margin-top: 30px;
    }
    .m-h-50 {
        margin-top: 50px;
    }
    .table {
        width: 100%;
        border-collapse: collapse;
    }
    .table th, .table td {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }
    .table th {
        background-color: #f2f2f2;
    }
    .text-right {
        text-align: right;
    }
    .small {
        font-size: 14px;
    }
    </style>
    '''

def htmltopdf(html_content):
    media_folder = os.path.join(settings.MEDIA_ROOT, 'Invoice')
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
    timestampval = int(round(time.time() * 100000))
    pdf_file_path = os.path.join(media_folder, f'{timestampval}.pdf')
    pdPath = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Path to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=pdPath)
    # config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }
    try:
        pdfkit.from_string(html_content, pdf_file_path, configuration=config, options=options)
        logging.info(f"PDF generated at: {pdf_file_path}")
        return pdf_file_path
    except Exception as e:
        logging.error(f"Error generating PDF: {e}")
        return ''
    
def send_email_with_document(emailid, cc_list, bcc_list, attachment_list, sub, html_content, record):
    email = EmailMessage(
        subject=sub,
        body=html_content,
        from_email='iverify@droidal.com',
        to=[emailid],
        cc=cc_list,
        bcc=bcc_list,
    )
    email.content_subtype = "html"  # Ensure the email is sent as HTML

    for attachment_path in attachment_list:
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment_file:
                attachment_content = attachment_file.read()
                attachment_name = os.path.basename(attachment_path)
                email.attach(attachment_name, attachment_content, 'application/pdf')

    try:
        email.send()
        print("Email sent successfully!....")

        
        
        # Update the ev_status to "Completed"
        record.ev_status = "Completed"
        record.ev_closed_createddatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        record.save()  # Save the updated record to the database

    except Exception as e:
        print(f"Error sending email: {e}")





def send_email_with_attachment(emailid, attachment_file):
    email = EmailMessage(
        subject='Invoice - Attached',
        body='Please find the attached Invoice for the given request',
        from_email='iverify@droidal.com',
        to=[emailid],
    )

    if attachment_file:
        try:
            email.attach_file(attachment_file)
            email.send()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
    else:
        print("Attachment file not found.")

@csrf_exempt
def sendinvoicerec(request):
    if request.method == 'POST':
        htmlcontent = request.POST.get('htmlcontent')
        emailid = request.POST.get('emailid').strip()
        
        if not emailid:
            return HttpResponse('Invalid email ID', status=400)
        
        htmlhead = '''<html><head><title>Invoice Print Preview</title></head><body>'''
        htmllink = htmlbootstraplink()
        htmlendbody = '''</body></html>'''
        htmlfinalcontent = htmlhead + htmllink + htmlcontent + htmlendbody
        
        pdfpath = htmltopdf(htmlfinalcontent)
        
        if not pdfpath:
            return HttpResponse('Failed to generate PDF', status=500)
        
        send_email_with_attachment(emailid, pdfpath)
        return HttpResponse('Mail Sent Successfully.')
    else:
        return HttpResponse('Invalid request method', status=405)


@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        htmlcontent = request.POST.get('htmlcontent')
        request_id = request.POST.get('request_id')

        htmlhead = '''<html><head><title>Invoice Print Preview</title></head><body>'''
        htmllink = htmlbootstraplink()
        htmlendbody = '''</body></html>'''
        htmlfinalcontent = htmlhead + htmllink + htmlcontent + htmlendbody
        
        pdfpath = htmltopdf(htmlfinalcontent)
        
        if not pdfpath:
            logging.error('Failed to generate PDF')
            return HttpResponse('Failed to generate PDF', status=500)

        try:
            form = get_object_or_404(UpstreamForm, request_id=request_id)
            form.invoice_pdf_path = pdfpath
            form.save()
            
            return JsonResponse({'pdfpath': pdfpath})
        except UpstreamForm.DoesNotExist:
            logging.error('No UpstreamForm matches the given query.')
            return HttpResponse('Failed to process PDF', status=500)
    else:
        return HttpResponse('Invalid request method', status=405)
    







@csrf_exempt
def save_dates_view(request):
    """
    This view handles POST requests that contain dates for multiple files.
    It saves these dates into the respective fields in the database using the request_id.
    """
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Get the request_id from the data
            request_id = data.get('request_id')

            # Print request_id for debugging purposes
            print(f"Request ID: {request_id}")

            # Ensure request_id is provided
            if not request_id:
                return JsonResponse({'error': 'Request ID is required'}, status=400)

            # Fetch the object using request_id (adjust the query as needed)
            obj = get_object_or_404(UpstreamForm, request_id=request_id)

            # Helper function to clean and validate dates
            def clean_date(date_str):
                if date_str and date_str != "":
                    # Return the date string if it's not empty
                    return date_str
                return None  # Return None for empty dates

            # Extract and clean date values from the request data
            file1_from_date = clean_date(data.get('file1_from_date'))
            file1_to_date = clean_date(data.get('file1_to_date'))
            file2_from_date = clean_date(data.get('file2_from_date'))
            file2_to_date = clean_date(data.get('file2_to_date'))
            file3_from_date = clean_date(data.get('file3_from_date'))
            file3_to_date = clean_date(data.get('file3_to_date'))
            file4_from_date = clean_date(data.get('file4_from_date'))
            file4_to_date = clean_date(data.get('file4_to_date'))
            file5_from_date = clean_date(data.get('file5_from_date'))
            file5_to_date = clean_date(data.get('file5_to_date'))
            file6_from_date = clean_date(data.get('file6_from_date'))
            file6_to_date = clean_date(data.get('file6_to_date'))
            file7_from_date = clean_date(data.get('file7_from_date'))
            file7_to_date = clean_date(data.get('file7_to_date'))
            file8_from_date = clean_date(data.get('file8_from_date'))
            file8_to_date = clean_date(data.get('file8_to_date'))
            file9_from_date = clean_date(data.get('file9_from_date'))
            file9_to_date = clean_date(data.get('file9_to_date'))
            file10_from_date = clean_date(data.get('file10_from_date'))
            file10_to_date = clean_date(data.get('file10_to_date'))

            # Print cleaned dates for debugging
            print(f"File 1 From Date: {file1_from_date}, File 1 To Date: {file1_to_date}")
            print(f"File 2 From Date: {file2_from_date}, File 2 To Date: {file2_to_date}")

            # Save each date into its corresponding field in the model
            obj.misc1_start_date = file1_from_date
            obj.misc1_end_date = file1_to_date
            obj.misc2_start_date = file2_from_date
            obj.misc2_end_date = file2_to_date
            obj.misc3_start_date = file3_from_date
            obj.misc3_end_date = file3_to_date
            obj.misc4_start_date = file4_from_date
            obj.misc4_end_date = file4_to_date
            obj.misc5_start_date = file5_from_date
            obj.misc5_end_date = file5_to_date
            obj.misc6_start_date = file6_from_date
            obj.misc6_end_date = file6_to_date
            obj.misc7_start_date = file7_from_date
            obj.misc7_end_date = file7_to_date
            obj.misc8_start_date = file8_from_date
            obj.misc8_end_date = file8_to_date
            obj.misc9_start_date = file9_from_date
            obj.misc9_end_date = file9_to_date
            obj.misc10_start_date = file10_from_date
            obj.misc10_end_date = file10_to_date

            # Save the updated model instance to the database
            obj.save()

            # Return success response
            return JsonResponse({'status': 'success'})

        except Exception as e:
            # Handle exceptions and return error message if something goes wrong
            print(f"Error: {e}")  # Log the error for debugging
            return JsonResponse({'error': str(e)}, status=500)

    # If the request method is not POST, return an error
    return JsonResponse({'error': 'Invalid request method'}, status=400)






def view_pdf(request):
    pdf_path = unquote(request.GET.get('pdfpath', ''))
    if not pdf_path:
        raise Http404('PDF file not found')

    pdf_full_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
    if os.path.exists(pdf_full_path):
        with open(pdf_full_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(pdf_full_path)}"'
            return response
    else:
        raise Http404('PDF file not found')



@csrf_exempt
def senddocumentmail(request):
    if request.method == 'POST':
        # Get all the fields from the frontend request
        htmlcontent = request.POST.get('htmlcontent')  # This is the HTML content from the frontend
        emailid = request.POST.get('emailid')
        bcc = request.POST.get('bcc')
        cc = request.POST.get('cc')
        sub = request.POST.get('sub')
        msg = request.POST.get('msg')
        requestid = request.POST.get('request_id')
        filepaths = request.POST.getlist('filepaths[]')

        try:
            # Fetch the request data
            getdata = UpstreamForm.objects.get(request_id=requestid)
        except UpstreamForm.DoesNotExist:
            return HttpResponse('UpstreamForm with the given request_id does not exist', status=404)

        # Fetch the saved PDF path (Invoice PDF) from the model
        pdfpath = getdata.invoice_pdf_path

        # Split cc and bcc lists if provided
        cc_list = cc.split(',') if cc else []
        bcc_list = bcc.split(',') if bcc else []

        # Helper function to construct a file URL
        def construct_file_url(path):
            file_url = request.build_absolute_uri(f'{settings.MEDIA_URL}{quote(path)}')
            file_url = file_url.replace('/media//media/', '/media/')
            file_url = file_url.replace('%2520', '%20')  # Correct space encoding
            return file_url

        # Build document links from filepaths
        file_links = []
        for filepath in filepaths:
            file_url = construct_file_url(filepath)
            file_links.append(f"<a href='{file_url}' target='_blank'>{os.path.basename(filepath)}</a>")

        # Create unique list of document links
        file_links = list(dict.fromkeys(file_links))
        file_links_html = "<br>".join(file_links)

        # Fetch the invoice PDF URL and create a clickable link
        if pdfpath:
            invoice_url = construct_file_url(pdfpath)
            invoice_link_html = f"<strong>Invoice PDF:</strong> <a href='{invoice_url}' target='_blank'>View Invoice</a>"

        # Create email body by combining the frontend HTML content and the links
        htmlfinalcontent = f"""
        <html>
        <body>
            {msg}  <!-- Include the HTML content from the frontend -->
            <br><br>
            <strong>Document Links:</strong><br>
            {file_links_html}
            <br><br>
            {invoice_link_html}
        </body>
        </html>
        """

        # Send the email with the combined HTML content
        send_email_without_attachment(emailid, cc_list, bcc_list, sub, htmlfinalcontent, getdata)

        return HttpResponse('Mail Sent Successfully.')
    else:
        return HttpResponse('Invalid request method', status=405)


def send_email_without_attachment(emailid, cc_list, bcc_list, sub, html_content, record):
    # Create the email
    email = EmailMessage(
        subject=sub,
        body=html_content,
        from_email='iverify@droidal.com',
        to=[emailid],
        cc=cc_list,
        bcc=bcc_list,
    )
    email.content_subtype = "html"  # Ensure the email is sent as HTML

    try:
        # Send the email
        email.send()
        print("Email sent successfully!")
        print("Hi")

        # Update the ev_status to "Completed"
        record.ev_status = "Completed"
        record.ev_closed_createddatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        record.save()  # Save the updated record to the database

    except Exception as e:
        print(f"Error sending email: {e}")




    
@csrf_exempt
def send_email_view(sub,mailtype,toaddr,emailusername,evid):
    subject = sub
    message = sub
    from_email = 'iverify@droidal.com'
    recipient_list = [toaddr]
    if mailtype=="new": 
        template_path = 'requestevmail.html'
    else:
        template_path = 'assignemail.html'
    context = {
        'username': emailusername,  
        'recordid':evid
    }

    email_html = render_to_string(template_path, context)

    send_mail(subject, message, from_email, recipient_list,html_message=email_html)


@csrf_exempt
def deleteupstream(request, id):
    if request.method == 'POST':
        try:
            data = UpstreamForm.objects.get(request_id=id)
            data.delete()
            return JsonResponse({'status': 'success'})
        except UpstreamForm.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Request not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
def get_total_pages(filename):
    static_folder = 'media/tempfiles'
    pdf_file_path = os.path.join(static_folder, filename)
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            return num_pages
    except Exception as e:
        print(f"Error: {e}")
        return 0

@csrf_exempt
def calculatepdfpage(request):
    if request.method == 'POST':
        formdata = request.POST
        requestid = formdata.get('requestid')
        miscname = formdata.get('miscname').strip()
        uploaded_file = request.FILES['miscfiles']

        static_folder = 'media/tempfiles'
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        file_path = os.path.join(static_folder, uploaded_file.name)
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            updatedata = UpstreamForm.objects.get(request_id=requestid)
        except UpstreamForm.DoesNotExist:
            return JsonResponse({'error': 'UpstreamForm with given request_id does not exist'}, status=404)

        setattr(updatedata, miscname, file_path)
        num_pages = get_total_pages(uploaded_file.name)

        # Extract the misc number from miscname (e.g., misc2_path -> misc2_pages)
        if '_path' in miscname:
            misc_num = miscname.replace('_path', '')
            page_field = f'{misc_num}_pages'
            setattr(updatedata, page_field, num_pages)

        # Calculate total pages and total amount
        total_pages = sum([
            getattr(updatedata, f'misc{i}_pages', 0) for i in range(1, 11)
        ])
        updatedata.total_pages = total_pages
        total_amount = total_pages * 1.5
        updatedata.total_amount = total_amount
        updatedata.balance = total_amount

        updatedata.save()

        return JsonResponse({'num_pages': num_pages, 'total_pages': total_pages, 'total_amount': total_amount})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


    


@login_required
def editupstream(request,id):
    if request.method == 'GET':
        overalldata = UpstreamForm.objects.get(request_id=id)
        context = {'data': overalldata}
        overalldata.approve_doc_status='on'
        if overalldata.approve_doc_status=='on':
            return render(request,'editupstream.html',context)
        else:
            return render(request,'approveupstream.html',context)
    if request.method == 'POST':
        formdata = request.POST 
        if "approval-checkbox" in formdata:
            
            uploaded_file = request.FILES['approval-file']
            # Define the path where you want to save the file inside the 'static' folder
            static_folder = 'static/uploads' 
            file_path = os.path.join(static_folder, uploaded_file.name)
             

            # Save the file
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk) 
            updatedata = UpstreamForm.objects.get(request_id=id) 
            updatedata.approve_doc_status =  formdata['approval-checkbox']
            updatedata.approve_doc_path =  file_path
            updatedata.save()
        return HttpResponseRedirect('/registration/')

@csrf_exempt  
def upstreamassignuser(request,id,aid):
    if request.method == "GET":       
        updatedata = UpstreamForm.objects.get(request_id=id) 
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
        updatedata.save()
        send_email_view('New Record Assigned','assigned',asingedemail,asingedusername,id)
        return HttpResponseRedirect('/registration/')
    

@login_required
def indexregisterupstreampage(request):
    if request.session.get('usertype') == 'admin':
        overalldata = UpstreamForm.objects.all().order_by('-request_id')
    elif request.session.get('usertype') == 'Internal-user':
        user_id = request.session.get('uid')
        user_details = UserDetails.objects.get(user_id=user_id)
        user_name = user_details.user_username
        overalldata = UpstreamForm.objects.filter(ev_assigned_to=user_name).order_by('-request_id')
    else:
        overalldata = UpstreamForm.objects.none()  # No data for other users
    
    userdata = UserDetails.objects.filter(user_Type='Internal-user')
    
    # Create a dictionary to store the files associated with each request
    files_dict = {}
    
    for data in overalldata:
        files_dict[data.request_id] = [file.file_path.name for file in RequestFile.objects.filter(request=data)]
    
    context = {
        'datas': overalldata,
        'users': userdata,
        'files_dict': files_dict
    }
    
    return render(request, 'indexupstream.html', context)



def download_all_pdfs(request, request_id):
    # Query all the files associated with this request
    files = RequestFile.objects.filter(request_id=request_id)

    # Create a temporary ZIP file
    zip_filename = f"request_{request_id}_pdfs.zip"
    zip_file_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
    
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for file_obj in files:
            # Use only the relative path from the database, and prepend the MEDIA_ROOT
            file_path = os.path.join(settings.MEDIA_ROOT, str(file_obj.file_path))
            
            if os.path.exists(file_path):
                zip_file.write(file_path, os.path.basename(file_path))
            else:
                print(f"File not found: {file_path}")  # Debugging output

    # Serve the ZIP file
    if os.path.exists(zip_file_path):
        with open(zip_file_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={zip_filename}'
            return response
    else:
        return HttpResponse("Error: ZIP file could not be created.", status=500)




@csrf_exempt
def update_request_status(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        assigned_to = request.POST.get('assigned_to')
        status = request.POST.get('status')
 
        # Check if the assigned_to value exceeds the length limit
        if len(assigned_to) > 10:
            return JsonResponse({'success': False, 'message': 'Assigned to value is too long.'})
        
        # Debugging print statement
        print(f"Assigned to: {assigned_to}")

        try:
            
            request_form = UpstreamForm.objects.get(request_id=request_id)
            request_form.ev_assigned_to = assigned_to
            request_form.ev_status = status
            request_form.ev_assigned_createddatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            request_form.save()
           
            # Send email to the external requestor
            send_assigned_request_email(request_form.requestor_email, request_id, request_form.requestor_name, request_form.patient_first_name, request_form.patient_last_name)
           
            return JsonResponse({'success': True, 'message': 'Request updated successfully.'})
        except UpstreamForm.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Request not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
 
 
 
def send_assigned_request_email(external_requestor_email, request_id, requestor_name, patient_first_name, patient_last_name):

    patient_full_name = f"{patient_first_name} {patient_last_name}".strip()

    
    subject = f"{patient_full_name}'s request has been initiated"


    

    body = f"""\
Dear {requestor_name},

Your request for {patient_full_name} with {request_id} has been initiated. We will get back to you with further updates shortly
 
If you have any further questions or need immediate assistance, please feel free to contact our office at844-319-6137 or roi@urpt.com.

Thank you for your patience and understanding.
 
Best regards,
DroidPoint
"""
 
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[external_requestor_email]
    )
    try:
        email.send()
        print("Assigned request email sent successfully!")
    except Exception as e:
        print(f"Error sending assigned request email: {e}")

@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            request_id = data.get('request_id')
            status = data.get('status')
            remarks = data.get('remarks')

            request_form = UpstreamForm.objects.get(request_id=request_id)
            request_form.ev_status = status
            request_form.ev_remarks = remarks
            request_form.save()

            if status == "Rejected":
                send_error_notification_email(request_form)

            return JsonResponse({'success': True, 'message': 'Approval status updated successfully.'})
        except UpstreamForm.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Request not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




@csrf_exempt
def update_status2(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request_id = data.get('request_id')
        status = data.get('status')
        remarks = data.get('remarks')
        
        try:
            request_form = UpstreamForm.objects.get(request_id=request_id)
            request_form.ev_status = status
            request_form.ev_remarks = remarks
            request_form.ev_closed_createddatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            request_form.save()

            # Check if status is 'Error' and send an email
            if status == "Error":
                send_error_notification_email(request_form)

            return JsonResponse({'success': True})
        except UpstreamForm.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Request not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Function to send email notification if the status is 'Error'
def send_error_notification_email(request_form):
    subject = f"Request has been Rejected for Request ID: {request_form.request_id}"
    body = f"""
Dear {request_form.requestor_name},<br><br>

Your request has been rejected. Please see the notes below:<br><br>

- Request ID : {request_form.request_id}<br>
- Status : Rejected<br><br>
- Reason : {request_form.ev_remarks}<br><br>

If you have any additional questions or concerns, please reach out to <a href="mailto:roi@urpt.com">roi@urpt.com</a> or call <a href="tel:+18443196137">844-319-6137</a>.<br><br>

If a new request is needed, please upload it at <a href="https://droidpoint.droidal.com/external_request/">Request Form</a>.<br><br>

Best regards,<br>  
DroidPoint
"""
    send_mail(
        subject=subject,
        message='',  # Empty message since we're sending HTML content
        html_message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request_form.requestor_email],
        fail_silently=False,
    )
    print(f"Error email sent to {request_form.requestor_email}")




logger = logging.getLogger(__name__)

@csrf_exempt
def toggle_approval(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        approve_status = request.POST.get('approve_status')
        saveStatus = request.POST.get('saveStatus')
        print(approve_status)

        try:
            request_form = UpstreamForm.objects.get(request_id=request_id)
            request_form.approve_doc_status = approve_status
            request_form.ev_status = saveStatus
            print("Saved")
            request_form.save()

            return JsonResponse({'success': True, 'message': 'Approval status updated successfully.'})
        except UpstreamForm.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Request not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})






@csrf_exempt
def upstreamstatusupdatereg(request):
    if request.method == 'GET':
        form = request.GET
        id=form['remarkid']
        updatedata = UpstreamForm.objects.get(request_id=id)   
        now=datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S') 
        updatedata.ev_status=form['status']
        updatedata.ev_remarks=form['remarks'] 
        updatedata.ev_closed_createddatetime=formatted_date
        updatedata.save()
        return HttpResponseRedirect('/registration/')


@login_required
def welcomeupstreampage(request):
    # print(request.session.items())
    # if request.session.get('usertype') == 'Internal-user':
    #     user_id = request.session.get('uid')
    #     user_details = UserDetails.objects.get(user_id=user_id)
    #     # full_name = f"{user_details.user_firstname} {user_details.user_lastname}"
    #     user_name = user_details.user_username
        
    #     overalldata = UpstreamForm.objects.filter(ev_assigned_to=user_name).order_by('-request_id')
    # else: 
    overalldata = UpstreamForm.objects.order_by('-request_id')
        
    context = {'datas': overalldata}
    return render(request, 'welcomeupstream.html', context)


@csrf_exempt
def insert_upstream_form(request):
    if request.method == 'GET':
        return render(request, 'upstream_form.html')
    else:
        data = request.POST
        files = request.FILES

        # Check if the authorization file is in the request
        if 'authorization_file_upload' in files:
            authorization_file = files['authorization_file_upload']
            auth_folder = settings.MEDIA_ROOT
            auth_file_path = os.path.join(auth_folder, authorization_file.name)

            # Save the authorization file
            with open(auth_file_path, 'wb') as destination:
                for chunk in authorization_file.chunks():
                    destination.write(chunk)
        else:
            auth_file_path = None

        # Check if the request file is in the request
        if 'request_file' in files:
            request_file = files['request_file']
            request_folder = 'media/Requests'
            request_file_path = os.path.join(request_folder, request_file.name)

            # Save the request file
            with open(request_file_path, 'wb') as destination:
                for chunk in request_file.chunks():
                    destination.write(chunk)
        else:
            request_file_path = None

        now = datetime.now()
        formatted_date = timezone.now().strftime('%Y-%m-%d')

        # Create and save the form instance
        form = UpstreamForm( 
            request_date2 = formatted_date,
            patient_last_name=data.get('patient_last_name'),
            patient_first_name=data.get('patient_first_name'),
            patient_date_of_birth=data.get('patient_date_of_birth'),
            requestor_name=data.get('requestor_name'),
            requestor_email=data.get('requestor_email'),
            request_file=request_file_path
        )
        form.save()
        return HttpResponseRedirect('/registration/') 



@csrf_exempt
def external_request(request):
    if request.method == 'GET':
        return render(request, 'external_upstream_form.html')
    elif request.method == 'POST':
        data = request.POST

        # Handle empty date fields and ensure they are in the correct format
        patient_dob = data.get('patient_dob') if data.get('patient_dob') else None
        patient_from_date = data.get('patient_from_date') if data.get('patient_from_date') else None
        patient_to_date = data.get('patient_to_date') if data.get('patient_to_date') else None

        try:
            # Create the main request object
            form = UpstreamForm.objects.create(
                request_date2=timezone.now().strftime('%Y-%m-%d'),
                external_request_createddatetime=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                patient_last_name=data.get('patient_last_name'),
                patient_first_name=data.get('patient_first_name'),
                patient_date_of_birth=patient_dob,
                requestor_name=data.get('requestor_name'),
                requestor_email=data.get('requestor_email'),
                request_type=data.get('request_type'),
                company=data.get('company_name'),
                patient_from_date=patient_from_date,
                patient_to_date=patient_to_date,
                request_file='',  # This can be left blank if using a related model for files
            )
            print(f"Request created with ID: {form.pk}")

            # Generate the invoice number: format INV/year/month/day/request_id
            current_date = timezone.now()
            invoice_number = f"INV{current_date.year}{str(current_date.month).zfill(2)}{str(current_date.day).zfill(2)}{str(form.pk).zfill(2)}"
            print(f"Generated Invoice Number: {invoice_number}")

            # Save the invoice number in the database
            form.invoice_number = invoice_number
            form.save()
            print(f"Invoice number {invoice_number} saved for request ID: {form.pk}")

            # Process and save uploaded files
            static_folder = settings.MEDIA_ROOT
            # os.makedirs(static_folder, exist_ok=True)
            print("Files will be stored in:", static_folder)

            for key in request.FILES:
                uploaded_file = request.FILES[key]
                print(f"Processing file: {uploaded_file.name}")
                request_file_path = os.path.join(static_folder, uploaded_file.name)

                # Save the file
                with open(request_file_path, 'wb') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                print(f"File saved to: {request_file_path}")

                # Save file path in database
                request_file_instance = RequestFile.objects.create(
                    request=form,
                    file_path=request_file_path
                )
                print(f"File path saved in database with ID: {request_file_instance.pk}")

            # Send acknowledgment email
            send_acknowledgment_email(form.requestor_email, form.requestor_name, form.pk, form.patient_first_name, form.patient_last_name)

            # Return success response
            print("Returning success response.")
            return JsonResponse({'message': 'Request Added Successfully', 'request_id': form.pk, 'invoice_number': invoice_number}, status=200)
        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({'error': 'Error processing request', 'details': str(e)}, status=500)
    else:
        print("Invalid request method.")
        return JsonResponse({'error': 'Invalid request method'}, status=400)



        # else:
        #     messages.error(request, 'Invalid data or missing file upload.')
        #     return HttpResponseRedirect('/external_request/')
 
 
       
def send_acknowledgment_email(email, requestor_name, pk, patient_first_name, patient_last_name,):

    # Concatenate patient full name
    patient_full_name = f"{patient_first_name} {patient_last_name}".strip()

    subject =  f"Acknowledgment for Medical Record Request - {patient_full_name}"

    # Hardcode the base URL for local development
    # base_url = 'http://127.0.0.1:8000'  # Replace with your local URL if different
    base_url = 'https://droidpoint.droidal.com/'

    # Generate the track record URL dynamically
    track_url = reverse('track_record')  # Assuming you have a URL pattern named 'track_record'
    full_track_url = f"{base_url}{track_url}?id={urlsafe_base64_encode(force_bytes(pk))}"

    

    message = f"""\
Dear {requestor_name},
 
Thank you for reaching out to us with your request for medical records. 

We have received your request for {patient_full_name} and it is currently in line to be processed in the order received.
 
We will notify you once the process is started and once your records are sent electronically If you have any further questions or need immediate assistance, please feel free to contact our office at 844-319-6137 or via email at roi@urpt.com.

Your Request ID is : {pk}
 
You can track the status of your request by visiting the following link:
{full_track_url}
 

Thank you for your patience and understanding.
 
Best regards,
Upstream
"""
 
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        print("Acknowledgment email sent successfully!")
    except Exception as e:
        print(f"Error sending acknowledgment email: {e}")
        


logger = logging.getLogger(__name__)

@csrf_exempt
def handle_file_upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['miscfiles']
        request_id = request.POST['requestid']
        
        # Save the uploaded file
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        logger.info(f"File uploaded: {file_url}")

        # Count the number of pages in the PDF
        file_path = fs.path(filename)
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)
        logger.info(f"File {filename} has {num_pages} pages")

        # Retrieve the form associated with the request_id
        form = get_object_or_404(UpstreamForm, request_id=request_id)

        # Save the file path and page count to the form
        saved = False
        for i in range(1, 11):
            if getattr(form, f'misc{i}_path') == '':
                setattr(form, f'misc{i}_path', file_url)
                setattr(form, f'misc{i}_pages', num_pages)
                saved = True
                logger.info(f"Saved file to misc{i}_path")
                break

        if saved:
            # Update total pages and amount
            total_pages = sum([
                getattr(form, f'misc{i}_pages', 0) for i in range(1, 11)
            ])
            form.total_pages = total_pages
            total_amount = total_pages * 1.5
            form.total_amount = total_amount
            form.balance = total_amount
            form.save()
            logger.info(f"Updated form {form.request_id} with new file. Total pages: {total_pages}, Total amount: {total_amount}")
        else:
            logger.warning(f"No available misc_path found for form {form.request_id}")

        return JsonResponse({'file_url': file_url, 'num_pages': num_pages, 'total_pages': form.total_pages, 'total_amount': form.total_amount})
    
    logger.error("Invalid request method")
    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def update_total_pages(request):
    if request.method == 'POST':
        total_pages = request.POST.get('total_pages')
        request_id = request.POST.get('requestid')
        
        # Check if total_pages is provided and is a valid integer
        if total_pages is None or not total_pages.isdigit():
            return JsonResponse({'status': 'error', 'message': 'Invalid total pages value.'}, status=400)

        # Retrieve the form by request_id
        form = get_object_or_404(UpstreamForm, request_id=request_id)
        
        try:
            # Update the total pages and save the form
            form.total_pages = int(total_pages)
            form.save()
            return JsonResponse({'status': 'success', 'total_pages': form.total_pages})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Failed to update total pages.'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)






def get_existing_files(request, request_id):
    form = get_object_or_404(UpstreamForm, request_id=request_id)
    files = []

    for i in range(1, 11):  # Adjusted to include up to misc10
        file_url = getattr(form, f'misc{i}_path')
        if file_url:
            files.append({'url': file_url, 'pages': getattr(form, f'misc{i}_pages')})

    return JsonResponse({'files': files})

@csrf_exempt 
def delete_file(request):
    if request.method == 'POST':
        request_id = request.POST['requestid']
        file_url = request.POST['file_url']
        
        form = get_object_or_404(UpstreamForm, request_id=request_id)
        
        def remove_file(file_path_attr, pages_attr):
            if getattr(form, file_path_attr) == file_url:
                setattr(form, file_path_attr, '')
                setattr(form, pages_attr, 0)
                return True
            return False
        
        file_removed = (
            remove_file('misc1_path', 'misc1_pages') or
            remove_file('misc2_path', 'misc2_pages') or
            remove_file('misc3_path', 'misc3_pages') or
            remove_file('misc4_path', 'misc4_pages') or
            remove_file('misc5_path', 'misc5_pages') or
            remove_file('misc6_path', 'misc6_pages')
        )
        
        if file_removed:
            form.save()
            fs = FileSystemStorage()
            file_path = os.path.join(settings.MEDIA_ROOT, file_url.lstrip('/'))
            if os.path.exists(file_path):
                os.remove(file_path)
            return JsonResponse({'success': True})
        
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_pdf_page_count(file_path):
    reader = PdfReader(file_path)
    return len(reader.pages)



@csrf_exempt
def update_totals(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request_id = data.get('request_id')
        total_pages = data.get('total_pages')
        print(total_pages)
        print(total_amount)
        total_amount = data.get('total_amount')

        try:
            form = UpstreamForm.objects.get(request_id=request_id)
            form.total_pages = total_pages
            form.total_amount = total_amount
            form.balance = total_amount
            form.save()
            return JsonResponse({'success': True})
        except UpstreamForm.DoesNotExist:
            return JsonResponse({'error': 'UpstreamForm with given request_id does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
def get_latest_invoice(request, request_id):
    try:
        form = UpstreamForm.objects.get(request_id=request_id)
        pdf_path = form.invoice_pdf_path  # Adjust this field according to your model
        return JsonResponse({'pdfpath': pdf_path})
    except UpstreamForm.DoesNotExist:
        return JsonResponse({'error': 'No invoice found for the given request ID'}, status=404)
    


@csrf_exempt
def save_patient_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request_id = data.get('request_id')
        patient_no = data.get('patient_no')
        notes = data.get('notes')
        company = data.get('company')  # New field
        address1 = data.get('address1')  # New field
        address2 = data.get('address2')  # New field
        city = data.get('city')  # New field
        zip_code = data.get('zip_code')  # New field
        email = data.get('email')  # New field

        try:
            # Retrieve the record based on request_id
            patient_record = UpstreamForm.objects.get(request_id=request_id)

            # Update the record with the new data
            patient_record.patient_no = patient_no
            patient_record.notes = notes
            patient_record.company = company  # Update with new field
            patient_record.address1 = address1  # Update with new field
            patient_record.address2 = address2  # Update with new field
            patient_record.city = city  # Update with new field
            patient_record.zip_code = zip_code  # Update with new field
            patient_record.requestor_email = email

            # Save the updated record
            patient_record.save()

            return JsonResponse({'success': True})
        except UpstreamForm.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Record not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})





@login_required
def pricing_page(request):
    return render(request, 'pricing.html')




@csrf_exempt
def save_charging_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        state = data.get('state')
        category = data.get('category')
        charges = data.get('charges', [])

        if not state or not category:
            return JsonResponse({'status': 'fail', 'message': 'State and category are required.'})

        try:
            charging_list, created = ChargingList.objects.get_or_create(state=state, category=category)

            for charge in charges:
                title = charge['title']
                value = charge['value']

                if hasattr(charging_list, title):
                    setattr(charging_list, title, value)

            charging_list.save()
            return JsonResponse({'status': 'success', 'message': 'Data saved successfully!'})

        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)})

    return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})



def get_charging_data_view(request):
    if request.method == "POST":
        state = request.POST.get('state')
        category = request.POST.get('category')

        if state and category:
            try:
                charging_list = ChargingList.objects.get(state=state, category=category)
                
                # Collecting all relevant fields
                data = {
                    'Base Fare': charging_list.base_fare,
                    'Minimum Fee': charging_list.minimum_fee,
                    'Flat Fee': charging_list.flat_fee,
                    'Free For': charging_list.free_for,
                    'Per Page': charging_list.per_page,
                    'Fee Limit': charging_list.fee_limit,
                    'Fee Limit For Mail': charging_list.fee_limit_for_mail,
                    'Fee Limit For Electronic': charging_list.fee_limit_for_electronic,
                    '1 Page': charging_list.page_1,
                    '1 to 5 Pages': charging_list.page_1_to_5,
                    '1 to 10 Pages': charging_list.page_1_to_10,
                    '1 to 20 Pages': charging_list.page_1_to_20,
                    '1 to 25 Pages': charging_list.page_1_to_25,
                    '1 to 30 Pages': charging_list.page_1_to_30,
                    '1 to 40 Pages': charging_list.page_1_to_40,
                    '1 to 50 Pages': charging_list.page_1_to_50,
                    '1 to 80 Pages': charging_list.page_1_to_80,
                    '1 to 100 Pages': charging_list.page_1_to_100,
                    '1 to 150 Pages': charging_list.page_1_to_150,
                    '1 to 250 Pages': charging_list.page_1_to_250,
                    '1 to 1000 Pages': charging_list.page_1_to_1000,
                    '2 to 30 Pages': charging_list.page_2_to_30,
                    '2 to 200 Pages': charging_list.page_2_to_200,
                    '11 to 20 Pages': charging_list.page_11_to_20,
                    '11 to 40 Pages': charging_list.page_11_to_40,
                    '11 to 50 Pages': charging_list.page_11_to_50,
                    '21 to 30 Pages': charging_list.page_21_to_30,
                    '21 to 40 Pages': charging_list.page_21_to_40,
                    '21 to 50 Pages': charging_list.page_21_to_50,
                    '21 to 60 Pages': charging_list.page_21_to_60,
                    '21 to 100 Pages': charging_list.page_21_to_100,
                    '21 to 500 Pages': charging_list.page_21_to_500,
                    '26 to 100 Pages': charging_list.page_26_to_100,
                    '26 to 350 Pages': charging_list.page_26_to_350,
                    '31 to 100 Pages': charging_list.page_31_to_100,
                    '101 to 200 Pages': charging_list.page_101_to_200,
                    'Above 5 Pages': charging_list.above_5_pages,
                    'Above 10 Pages': charging_list.above_10_pages,
                    'Above 20 Pages': charging_list.above_20_pages,
                    'Above 25 Pages': charging_list.above_25_pages,
                    'Above 30 Pages': charging_list.above_30_pages,
                    'Above 40 Pages': charging_list.above_40_pages,
                    'Above 50 Pages': charging_list.above_50_pages,
                    'Above 60 Pages': charging_list.above_60_pages,
                    'Above 80 Pages': charging_list.above_80_pages,
                    'Above 100 Pages': charging_list.above_100_pages,
                    'Above 150 Pages': charging_list.above_150_pages,
                    'Above 200 Pages': charging_list.above_200_pages,
                    'Above 250 Pages': charging_list.above_250_pages,
                    'Above 350 Pages': charging_list.above_350_pages,
                    'Above 500 Pages': charging_list.above_500_pages,
                    'Above 1000 Pages': charging_list.above_1000_pages,
                    'First Hour': charging_list.first_hour,
                    'Each Additional Hour': charging_list.each_additional_hour,
                    'Required Fee': charging_list.required_fee,
                    'Amount': charging_list.amount,
                    'Optional Fee': charging_list.optional_fee,
                    'Amount 1': charging_list.amount_1,
                    'Optional Fee 1': charging_list.optional_fee_1,
                    'Amount 2': charging_list.amount_2,
                    'Minimum Fee': charging_list.minimum_fee,
                    'Email': charging_list.email,
                    'Mail': charging_list.mail,
                }

                return JsonResponse({"status": "success", "data": data})
            except ChargingList.DoesNotExist:
                return JsonResponse({"status": "fail", "message": "No data found for the selected state and category."})
        else:
            return JsonResponse({"status": "fail", "message": "State and Category are required."})
    else:
        return JsonResponse({"status": "fail", "message": "Invalid request method."})


@csrf_exempt
def track_record(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request_id = request.POST.get('request_id')
        
        try:
            
            record = UpstreamForm.objects.get(requestor_email=email, request_id=request_id)
            return redirect('track_result', record_id=record.request_id)
        except UpstreamForm.DoesNotExist:
            context = {
                'error': 'No records found for the provided email and request ID.',
                'lottie_animation': True
            }
            return render(request, 'track_record.html', context)

    return render(request, 'track_record.html')

def track_result(request, record_id):
    try:
        
        record = UpstreamForm.objects.get(request_id=record_id)
        context = {'record': record}
    except UpstreamForm.DoesNotExist:
        context = {'error': 'No Records found !'}
    
    return render(request, 'track_result.html', context)


   
@csrf_exempt
def website(request):
    return render(request,'website.html')














def calculate_total_amount(request, state, category, total_pages):
    try:
        special_categories = ["Patient", "Doctor's office", "Non-billable other", "Deposition"]

        if category in special_categories:
            charging_lists = ChargingList.objects.filter(category=category)
            if not charging_lists.exists():
                return JsonResponse({'error': f'No charges found for the category {category}.'}, status=404)
        else:
            charging_lists = ChargingList.objects.filter(state=state, category=category)

            if category == 'workers compensation' and state == 'Utah':
                charging_lists = ChargingList.objects.filter(state=state, category='workers compensation')

            if category == 'DDS' and state == 'Utah':
                charging_lists = ChargingList.objects.filter(state=state, category='general')

            if not charging_lists.exists():
                charging_lists = ChargingList.objects.filter(state=state, category='general')

                if not charging_lists.exists():
                    return JsonResponse({'error': 'Charging list not found for the given state and category.'}, status=404)

        calculation_details = []
        total_value = 0
        total_paper_charge = 0
        total_additional_fees = 0
        flat_fee_applied = False  

        try:
            request_data = json.loads(request.body)
            optional_fees = request_data.get('optional_fees', [])
            hours = request_data.get('hours', 0)  # Get the hours value from request
            delivery_method = request_data.get('delivery_method', None)  # Get delivery method from request

        except json.JSONDecodeError:
            optional_fees = []
            hours = 0
            delivery_method = None

        

        for charging_list in charging_lists:
            paper_charge, additional_fees_total = calculate_total_value(
                int(total_pages), charging_list, calculation_details, flat_fee_applied, optional_fees
            )
            total_paper_charge += paper_charge
            total_additional_fees += additional_fees_total
            total_value += paper_charge + additional_fees_total

            if charging_list.flat_fee:
                flat_fee_applied = True

            # Deposition hours calculation
            if category == 'Deposition' and hours > 0:
                if hours == 1 and charging_list.first_hour:
                    total_value += float(charging_list.first_hour)
                    calculation_details.append({
                        'label': 'First Hour',
                        'value': float(charging_list.first_hour)
                    })
                elif hours > 1 and charging_list.each_additional_hour:
                    first_hour_value = float(charging_list.first_hour) if charging_list.first_hour else 0
                    additional_hour_value = float(charging_list.each_additional_hour) * (hours - 1)
                    total_value += first_hour_value + additional_hour_value
                    calculation_details.append({
                        'label': 'First Hour',
                        'value': first_hour_value
                    })
                    calculation_details.append({
                        'label': 'Additional Hour',
                        'value': additional_hour_value
                    })

        # Handle optional fees
        for fee in optional_fees:
            fee_amount = float(fee.get('value', 0))
            total_additional_fees += fee_amount
            total_value += fee_amount
            calculation_details.append({
                'label': fee.get('type', 'Optional Fee'),
                'value': fee_amount
            })


        for charging_list in charging_lists:
            if charging_list.fee_limit:
                fee_limit = float(charging_list.fee_limit)
                if total_value > fee_limit:
                    total_value = fee_limit
                    # Clear any existing calculation details and append only the fee limit details
                    calculation_details = [{
                        'label': 'Fee Limit Applied',
                        'value': fee_limit
                    }]
                    break 

        # Apply fee limit based on delivery method
        if state == "South Carolina" and category == "general": 
            for charging_list in charging_lists:
                if delivery_method == "Mail":
                    fee_limit = float(charging_list.fee_limit_for_mail)
                    if total_value > fee_limit:
                        total_value = fee_limit
                        calculation_details = [{
                            'label': 'Fee Limit Applied (Mail)',
                            'value': fee_limit
                        }]
                        break

                elif delivery_method == "Electronic":
                    fee_limit = float(charging_list.fee_limit_for_electronic)
                    if total_value > fee_limit:
                        total_value = fee_limit
                        calculation_details = [{
                            'label': 'Fee Limit Applied (Electronic)',
                            'value': fee_limit
                        }]
                        break
        
        
        for charging_list in charging_lists:
            if charging_list.minimum_fee:
                minimum_fee = float(charging_list.minimum_fee)
                if total_value < minimum_fee:
                    total_value = minimum_fee
                    # Clear existing calculation details and only append the minimum fee details
                    calculation_details = [{
                        'label': 'Minimum Fee Applied',
                        'value': minimum_fee
                    }]
                    break
            



        print(f"Total value calculated: {total_value}")
        print(f"Calculation details: {calculation_details}") 

        return JsonResponse({
            'total_amount': total_value,
            'total_paper_charge': total_paper_charge,
            'total_additional_fees': total_additional_fees,
            'calculation_details': calculation_details
        })
    except ChargingList.DoesNotExist:
        return JsonResponse({'error': 'Charging list not found for the given state and category.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



    





def calculate_total_value(total_pages, charging_list, calculation_details, flat_fee_applied, optional_fees=None):
    total_value = 0
    additional_page_cost = 0
    available_charges = {}

    

    # Populate available_charges dictionary
    for field in charging_list._meta.fields:
        value = getattr(charging_list, field.name)
        if value is not None and field.name.startswith(('page_', 'above_')):
            try:
                available_charges[field.name] = float(value)
            except ValueError:
                continue

    remaining_pages = total_pages

    # Apply flat fee if applicable
    if charging_list.flat_fee and not flat_fee_applied:
        total_value += float(charging_list.flat_fee)
        calculation_details.append({
            'label': 'Flat Fee Applied',
            'value': float(charging_list.flat_fee)
        })
        flat_fee_applied = True

    # Apply base fare or calculate page range cost
    if charging_list.base_fare:
        base_fare = float(charging_list.base_fare)
        initial_page_range_cost = 0
        base_fare_applied = False
    
        # Calculate the cost based on page ranges
        if 'page_1' in available_charges and remaining_pages > 0:
            pages_to_charge = min(1, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_5' in available_charges and remaining_pages > 0:
            pages_to_charge = min(5, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_10' in available_charges and remaining_pages > 0:
            pages_to_charge = min(10, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_20' in available_charges and remaining_pages > 0:
            pages_to_charge = min(20, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_25' in available_charges and remaining_pages > 0:
            pages_to_charge = min(25, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_30' in available_charges and remaining_pages > 0:
            pages_to_charge = min(30, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_40' in available_charges and remaining_pages > 0:
            pages_to_charge = min(40, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_50' in available_charges and remaining_pages > 0:
            pages_to_charge = min(50, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_80' in available_charges and remaining_pages > 0:
            pages_to_charge = min(80, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_100' in available_charges and remaining_pages > 0:
            pages_to_charge = min(100, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_150' in available_charges and remaining_pages > 0:
            pages_to_charge = min(150, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_250' in available_charges and remaining_pages > 0:
            pages_to_charge = min(250, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })

        elif 'page_1_to_1000' in available_charges and remaining_pages > 0:
            pages_to_charge = min(1000, remaining_pages)
            total_value += base_fare
            remaining_pages -= pages_to_charge
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': base_fare
            })
        
               # Continue with the calculation for the remaining pages after base fare is applied
        additional_page_cost = calculate_remaining_page_costs(remaining_pages, available_charges, calculation_details)
        total_value += additional_page_cost  
    else: 
        # Calculate the cost based on page ranges
        if 'page_1' in available_charges and remaining_pages > 0:
            pages_to_charge = min(1, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_5' in available_charges and remaining_pages > 0:
            pages_to_charge = min(5, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_5']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_10' in available_charges and remaining_pages > 0:
            pages_to_charge = min(10, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_10']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_20' in available_charges and remaining_pages > 0:
            pages_to_charge = min(20, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_20']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_25' in available_charges and remaining_pages > 0:
            pages_to_charge = min(25, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_25']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_30' in available_charges and remaining_pages > 0:
            pages_to_charge = min(30, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_30']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_40' in available_charges and remaining_pages > 0:
            pages_to_charge = min(40, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_40']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_50' in available_charges and remaining_pages > 0:
            pages_to_charge = min(50, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_50']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_80' in available_charges and remaining_pages > 0:
            pages_to_charge = min(80, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_80']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_100' in available_charges and remaining_pages > 0:
            pages_to_charge = min(100, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_100']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_150' in available_charges and remaining_pages > 0:
            pages_to_charge = min(150, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_150']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_250' in available_charges and remaining_pages > 0:
            pages_to_charge = min(250, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_250']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })

        elif 'page_1_to_1000' in available_charges and remaining_pages > 0:
            pages_to_charge = min(1000, remaining_pages)
            initial_page_range_cost = pages_to_charge * available_charges['page_1_to_1000']
            remaining_pages -= pages_to_charge
            total_value += initial_page_range_cost
            calculation_details.append({
                'label': f'Charge for {pages_to_charge} Page(s)',
                'value': initial_page_range_cost
            })
        
        additional_page_cost = calculate_remaining_page_costs(remaining_pages, available_charges, calculation_details)
        total_value += additional_page_cost

        


    if charging_list.email:
        total_value += float(charging_list.email)
        calculation_details.append({
            'label': 'Email',
            'value': float(charging_list.email)
        })

    if charging_list.mail:
        total_value += float(charging_list.mail)
        calculation_details.append({
            'label': 'Mail',
            'value': float(charging_list.mail)
        })

    # if charging_list.first_hour:
    #     total_value += float(charging_list.first_hour)
    #     calculation_details.append({
    #         'label': 'First Hour',
    #         'value': float(charging_list.first_hour)
    #     })

    # if charging_list.each_additional_hour:
    #     total_value += float(charging_list.each_additional_hour)
    #     calculation_details.append({
    #         'label': 'For Each Additional Hour',
    #         'value': float(charging_list.each_additional_hour)
    #     })

    # Apply minimum fee if applicable


    if charging_list.per_page:
        per_page = float(charging_list.per_page)
        total_value = per_page * total_pages 
        calculation_details.append({
            'label': f'Charge for {total_pages} Page(s)', 
            'value': total_value
        })

    # # Check and apply fee limit if applicable
    # if charging_list.fee_limit:
    #     fee_limit = float(charging_list.fee_limit)
    #     if total_value > fee_limit:
    #         total_value = fee_limit
    #         calculation_details.append({
    #             'label': 'Fee Limit Applied',
    #             'value': fee_limit
    #         })


    
    # Calculate additional fees separately
    total_additional_fees = 0
    if charging_list.amount:
        total_additional_fees += float(charging_list.amount)
        calculation_details.append({
            'label': str(charging_list.required_fee),
            'value': float(charging_list.amount)
        })

    if charging_list.amount_1:
        total_additional_fees += float(charging_list.amount_1)
        calculation_details.append({
            'label': str(charging_list.optional_fee),
            'value': float(charging_list.amount_1)
        })

    if charging_list.amount_2:
        total_additional_fees += float(charging_list.amount_2)
        calculation_details.append({
            'label': str(charging_list.optional_fee_1),
            'value': float(charging_list.amount_2)
        })

    # Include fees from frontend
    # if optional_fees:
    #     for fee in optional_fees:
    #         fee_type = fee['type']
    #         fee_value = float(fee['value'])

    #         total_additional_fees += fee_value
    #         calculation_details.append({
    #             'label': f'Additional Fee: {fee_type}',
    #             'value': fee_value
    #         })

    return total_value, total_additional_fees















def calculate_remaining_page_costs(remaining_pages, available_charges, calculation_details):
    additional_page_cost = 0
    

    # if 'page_1' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(1, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1',
    #         'value': cost
    #     })

    # if 'page_1_to_5' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(5, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_5']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_5',
    #         'value': cost
    #     })

    # if 'page_1_to_10' in available_charges and remaining_pages > 0:
    #     # Correctly charge for pages within this range
    #     pages_to_charge = min(10, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_10']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_10',
    #         'value': cost
    #     })

    # if 'page_1_to_20' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(20, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_20']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_20',
    #         'value': cost
    #     })

    # if 'page_1_to_25' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(25, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_25']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_25',
    #         'value': cost
    #     })

    # if 'page_1_to_30' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(30, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_30']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_30',
    #         'value': cost
    #     })

    # if 'page_1_to_40' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(40, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_40']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_40',
    #         'value': cost
    #     })

    # if 'page_1_to_50' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(50, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_50']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_50',
    #         'value': cost
    #     })

    # if 'page_1_to_80' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(80, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_80']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_80',
    #         'value': cost
    #     })

    # if 'page_1_to_100' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(100, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_100']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_100',
    #         'value': cost
    #     })

    # if 'page_1_to_150' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(150, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_150']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_150',
    #         'value': cost
    #     })

    # if 'page_1_to_250' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(250, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_250']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_250',
    #         'value': cost
    #     })

    # if 'page_1_to_1000' in available_charges and remaining_pages > 0:
    #     pages_to_charge = min(1000, remaining_pages)
    #     cost = pages_to_charge * available_charges['page_1_to_1000']
    #     additional_page_cost += cost
    #     remaining_pages -= pages_to_charge
    #     calculation_details.append({
    #         'label': f'Charge for {pages_to_charge} page(s) at rate page_1_to_1000',
    #         'value': cost
    #     })

    if 'page_2_to_30' in available_charges and remaining_pages > 0:
        pages_to_charge = min(29, remaining_pages)
        cost = pages_to_charge * available_charges['page_2_to_30']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_2_to_200' in available_charges and remaining_pages > 0:
        pages_to_charge = min(199, remaining_pages)
        cost = pages_to_charge * available_charges['page_2_to_200']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_11_to_20' in available_charges and remaining_pages > 0:
        pages_to_charge = min(10, remaining_pages)
        cost = pages_to_charge * available_charges['page_11_to_20']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_11_to_40' in available_charges and remaining_pages > 0:
        pages_to_charge = min(30, remaining_pages)
        cost = pages_to_charge * available_charges['page_11_to_40']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_11_to_50' in available_charges and remaining_pages > 0:
        pages_to_charge = min(40, remaining_pages)
        cost = pages_to_charge * available_charges['page_11_to_50']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_21_to_30' in available_charges and remaining_pages > 0:
        pages_to_charge = min(10, remaining_pages)
        cost = pages_to_charge * available_charges['page_21_to_30']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_21_to_40' in available_charges and remaining_pages > 0:
        pages_to_charge = min(20, remaining_pages)
        cost = pages_to_charge * available_charges['page_21_to_40']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_21_to_50' in available_charges and remaining_pages > 0:
        pages_to_charge = min(30, remaining_pages)
        cost = pages_to_charge * available_charges['page_21_to_50']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_21_to_60' in available_charges and remaining_pages > 0:
        pages_to_charge = min(40, remaining_pages)
        cost = pages_to_charge * available_charges['page_21_to_60']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_21_to_100' in available_charges and remaining_pages > 0:
        pages_to_charge = min(80, remaining_pages)
        cost = pages_to_charge * available_charges['page_21_to_100']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_21_to_500' in available_charges and remaining_pages > 0:
        pages_to_charge = min(480, remaining_pages)
        cost = pages_to_charge * available_charges['page_21_to_500']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_26_to_100' in available_charges and remaining_pages > 0:
        pages_to_charge = min(75, remaining_pages)
        cost = pages_to_charge * available_charges['page_26_to_100']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_26_to_350' in available_charges and remaining_pages > 0:
        pages_to_charge = min(325, remaining_pages)
        cost = pages_to_charge * available_charges['page_26_to_350']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_31_to_100' in available_charges and remaining_pages > 0:
        pages_to_charge = min(70, remaining_pages)
        cost = pages_to_charge * available_charges['page_31_to_100']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'page_101_to_200' in available_charges and remaining_pages > 0:
        pages_to_charge = min(100, remaining_pages)
        cost = pages_to_charge * available_charges['page_101_to_200']
        additional_page_cost += cost
        remaining_pages -= pages_to_charge
        calculation_details.append({
            'label': f'Charge for {pages_to_charge} Page(s) ',
            'value': cost
        })

    if 'above_5_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_5_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_10_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_10_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_20_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_20_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_25_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_25_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_30_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_30_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_40_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_40_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_50_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_50_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_60_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_60_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_80_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_80_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_100_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_100_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_150_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_150_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_200_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_200_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_250_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_250_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_350_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_350_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_500_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_500_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    if 'above_1000_pages' in available_charges and remaining_pages > 0:
        cost = remaining_pages * available_charges['above_1000_pages']
        additional_page_cost += cost
        calculation_details.append({
            'label': f'Charge for {remaining_pages} Page(s) ',
            'value': cost
        })

    return additional_page_cost


