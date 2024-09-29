"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path 

from upstreamform.views import insert_upstream_form,welcomeupstreampage,indexregisterupstreampage,delete_file,get_latest_invoice, get_charging_data_view, save_charging_data, download_all_pdfs, update_total_pages, \
        editupstream,calculatepdfpage,get_total_pages,deleteupstream,external_request,upstreamassignuser,upstreamstatusupdatereg,get_existing_files, calculate_total_amount, \
        sendinvoicerec,senddocumentmail,updateauthapprove, website, update_request_status, toggle_approval, generate_pdf, update_status, view_pdf, handle_file_upload, update_totals, update_status2, track_record, track_result, save_patient_data, pricing_page, save_dates_view

urlpatterns = [ 
    path('',website),  
    path("external_request/",external_request),   
    path('website/',website),
    path('track_record/', track_record, name='track_record'),
    path('track_result/<int:record_id>/', track_result, name='track_result'), 


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)