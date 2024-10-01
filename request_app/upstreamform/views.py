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
        





@csrf_exempt
def track_record(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request_id = request.POST.get('request_id')
        
        try:
            
            record = UpstreamForm.objects.get(requestor_email=email, request_id=request_id)
            redirecturl = '/request-app/track_result/'+str(record.request_id)
            return redirect(redirecturl)
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