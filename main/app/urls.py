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
from register.views import Signup,login_page,logout_view, forgot_password, reset_password, code_verify, send_otp, \
    verify_email_otp, reset_password_update
from evrequest.views import evrequestpage,\
    deletereg,editreg,completereg,errorreg,assignuser,\
    inprogressreg,date_range_view,statusupdatereg,\
    analytics,updatefilerecord,userlist,userchecklist,daterange_view

from cas.views import insert_casform

from upstreamform.views import insert_upstream_form,welcomeupstreampage,indexregisterupstreampage,delete_file,get_latest_invoice, get_charging_data_view, save_charging_data, download_all_pdfs, update_total_pages, \
        editupstream,calculatepdfpage,get_total_pages,deleteupstream,external_request,upstreamassignuser,upstreamstatusupdatereg,get_existing_files, calculate_total_amount, \
        sendinvoicerec,senddocumentmail,updateauthapprove, website, update_request_status, toggle_approval, generate_pdf, update_status, view_pdf, handle_file_upload, update_totals, update_status2, track_record, track_result, save_patient_data, pricing_page, save_dates_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',Signup),
    path('',login_page),
    path('login/',login_page),
    path('forgot_password/',forgot_password),
    path('send-otp/', send_otp, name='send_otp'),
    path('reset_password/',reset_password),
    path('reset_password_update/',reset_password_update),
    path('verify_email_otp/', verify_email_otp, name='verify_email_otp'),
    path('code_verification/',code_verify),
    path('accounts/login/', auth_views.LoginView.as_view(), name='account_login'),  # Default login redirection
    path('welcome/',welcomeupstreampage),
    path('newev/',evrequestpage),
    path('registration/',indexregisterupstreampage),
    path('registeration/',indexregisterupstreampage),
    path('update_request_status/',update_request_status),
    path('updateStatus/', update_status),
    path('updateStatus2/', update_status2),
    path('toggle_approval/',toggle_approval),
    path('delete/<int:id>',deletereg),
    path('deleteupstream/<int:id>/',deleteupstream),
    path('edit/<int:id>',editupstream),
    path('complete/<int:id>',completereg),
    path('error/<int:id>',errorreg),
    path('inprogress/<int:id>',inprogressreg),
    path('logout/',logout_view),
    path('assignuser/<int:id>/<int:aid>',assignuser),
    path('daterange/', daterange_view, name='daterange_view'),
    path('statusupdatereg/',statusupdatereg,name='statusupdatereg'),
    path('analytics/',analytics),
    path("updatefilerecord/",updatefilerecord,name="updatefilerecord"),
    path("userlist/",userlist),
    path("userchecklist/",userchecklist), 
    path("insert_casform/",insert_casform),
    path("insert_upstream_form/",insert_upstream_form),
    path("calculatepdfpage/",calculatepdfpage),
    path("get_total_pages/",get_total_pages),   
    path('upstreamassignuser/<int:id>/<int:aid>',upstreamassignuser),
    path('upstreamstatusupdatereg/',upstreamstatusupdatereg,name='upstreamstatusupdatereg'),
    path('sendinvoicerec/',sendinvoicerec),
    path('generatepdf/', generate_pdf),
    path('senddocumentmail/',senddocumentmail),
    path('updateauthapprove/',updateauthapprove),
    path('viewpdf/', view_pdf, name='viewpdf'),
    path('handle_file_upload/', handle_file_upload, name='handle_file_upload'),
    path('get_existing_files/<int:request_id>/', get_existing_files, name='get_existing_files'),
    path('delete_file/', delete_file, name='delete_file'),
    path('update_totals/', update_totals, name='update_totals'),
    path('get_latest_invoice/<str:request_id>/', get_latest_invoice, name='get_latest_invoice'), 
    path('save_patient_data/', save_patient_data, name='save_patient_data'),
    path('pricing_page/', pricing_page, name='pricing_page'),
    path('get-charging-data/', get_charging_data_view, name='get_charging_data'),
    path('save_charging_data/', save_charging_data, name='save_charging_data'),
    path('calculate_total_amount/<str:state>/<str:category>/<int:total_pages>/', calculate_total_amount, name='calculate_total_amount'),
    path('download-all-pdfs/<int:request_id>/', download_all_pdfs, name='download_all_pdfs'),
    path('update_total_pages/', update_total_pages, name='update_total_pages'),
    path('save_dates/', save_dates_view, name='save_dates'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)