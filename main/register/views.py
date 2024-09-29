from django.contrib import messages
from django.conf import settings
from django.db import connection
from django.http import HttpResponse, response, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, login, authenticate
from django.core.mail import send_mail 
from django.template.loader import render_to_string 
import hashlib
import base64
import pyotp
import qrcode
import os
from .models import UserDetails
from django.contrib.auth.models import User
from django.middleware.csrf import get_token, rotate_token
import random
from django.http import JsonResponse
import logging
import json
from django.utils import timezone
import datetime

# Create your views here.

def send_email_view(toaddr, userName, mailpwd, qrpath):
    subject = 'Welcome to iVerify Portal!'
    message = 'Welcome to iverify portal'
    from_email = settings.DEFAULT_FROM_EMAIL  # Use the configured default sender
    recipient_list = [toaddr]

    template_path = 'welcomemail.html'  # Ensure this path is correct
    with open(qrpath, 'rb') as qr_code_file:
        qr_code_data = qr_code_file.read()
        qr_code_base64 = base64.b64encode(qr_code_data).decode('utf-8')
    context = {
        'username': userName,
        'mailpwd': mailpwd, 
        'portallink': 'https://droidpoint.droidal.com',
        'qr_code_base64': qr_code_base64,
    }

    # Render the HTML content of the email
    email_html = render_to_string(template_path, context)

    send_mail(subject, message, from_email, recipient_list, html_message=email_html)

    # return render(request, 'email_sent.html')

def logout_view(request):
    # Unset session variable
    if 'uid' in request.session:
        del request.session['uid']
        del request.session['username']

    logout(request)
    return HttpResponseRedirect('/login/')


# def md5_hash_password(raw_password):
#     # Convert the password to bytes before hashing
#     password_bytes = raw_password.encode('utf-8')

#     # Use the MD5 hash function
#     md5_hash = hashlib.md5(password_bytes)

#     # Get the hexadecimal representation of the hash
#     hashed_password = md5_hash.hexdigest()

#     return hashed_password



def hash_password(raw_password):
    return make_password(raw_password)




def verify_otp(secret_key, otp):
    totp = pyotp.TOTP(secret_key)
    return totp.verify(otp)

def qrcode_generate(username):

    # Generate a random base32 secret key (for TOTP)
    secret_key = pyotp.random_base32()

    # Create a TOTP object with the secret key
    totp = pyotp.TOTP(secret_key)

    # Generate the QR code URL for the secret key
    qr_code_url = totp.provisioning_uri(name='iverify', issuer_name='Droidal')

    # Generate the QR code image
    qr = qrcode.make(qr_code_url)
 
    
    static_folder = 'static/uploads' 
    filename=str(username)+'.png'
    qr_code_path = os.path.join(static_folder, filename)

    # Save the QR code image to a file
    qr.save(qr_code_path)

    return secret_key,qr_code_path


def Signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')

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
        encryptpass = hash_password(password)  # Use Django's password hashing

        # Check if the email already exists
        if UserDetails.objects.filter(user_email=email).exists():
            messages.error(request, 'Email already exists. Please choose a different one.')
            return HttpResponseRedirect('/signup/')

        # Check if the username already exists
        if UserDetails.objects.filter(user_username=user).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return HttpResponseRedirect('/signup/')

        secretkey, qrpath = qrcode_generate(user)
        try:
            userdet = UserDetails.objects.create(
                user_Type=designation,
                user_email=email,
                user_firstname=firstname,
                user_lastname=lastname,
                user_mobile=mobilenumber,
                user_company=organization,
                user_designation=designation,
                user_username=user,
                user_password=encryptpass,
                user_SecretKey=secretkey
            )
        except Exception as e:
            print(e)
        
        if userdet:
            send_email_view(email, user, password, qrpath)
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'signup.html')

def login_page(request):
    # Debugging: Print the CSRF token
    csrf_token = get_token(request)
    print("CSRF Token:", csrf_token)
    
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        # Check if the CSRF token is being sent in the POST request
        csrf_token_post = request.POST.get('csrfmiddlewaretoken')
        print("CSRF Token from POST:", csrf_token_post)
        
        form = request.POST

        # Handle MFA password verification
        if 'mfapassword' in form:
            mfapassword = form['mfapassword']
            mfasecretkey = form['mfasecretkey']
            mfauid = form['mfauid']
            # verifystatus = verify_otp(mfasecretkey, mfapassword)
            verifystatus = True
            
            if verifystatus:
                result = UserDetails.objects.filter(user_id=mfauid).first()
                if result:
                    uid = result.user_id
                    username = result.user_username
                    usertype = result.user_Type
                    
                    # Fetch or create the user object
                    user, created = User.objects.get_or_create(username=username)
                    
                    # Update session variables
                    request.session['uid'] = uid
                    request.session['username'] = username
                    request.session['usertype'] = usertype
                    request.session.modified = True

                    # Log in the user
                    login(request, user)
                    
                    return HttpResponseRedirect('/welcome/')
            else:
                messages.error(request, 'Invalid Passcode Given!')
                return render(request, 'login.html', {'form': form})
        
        else:
            username = form['user']
            password = form['password']
            remember_me = form.get('remember_me')

            result = UserDetails.objects.filter(user_username=username).first()
            if result and check_password(password, result.user_password):
                secretkey = result.user_SecretKey
                uid = result.user_id
                usertype = result.user_Type
                
                # Fetch or create the user object
                user, created = User.objects.get_or_create(username=username)
                
                request.session['usertype'] = usertype
                request.session.modified = True

                # Handle "Remember Me" functionality
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Session expires when the browser is closed

                # Log in the user
                login(request, user)
                
                return render(request, 'loginmfa.html', {'secret': secretkey, 'uid': uid})
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'login.html', {'form': form})
            

def forgot_password(request):
    return render(request, 'forgotpassword.html')

def reset_password(request):
    return render(request, 'resetpassword.html')

def code_verify(request):
    return render(request, 'codeverification.html')



def send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'success': False, 'message': 'Email is required.'})

            email = email.strip()

            # Fetch user with case-insensitive email
            user = UserDetails.objects.get(user_email__iexact=email)
            user_name = user.user_username

            otp = random.randint(1000, 9999)

            # Save the OTP and the current time in the session
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['otp_time'] = timezone.now().isoformat()  # Store as an ISO format string

            subject = 'Your Password Reset OTP'
            message = f'''Dear {user_name},

We received a request to reset your password for your [Your Company Name] account. To proceed with resetting your password, please use the following One-Time Password (OTP):

Your OTP: {otp}

This OTP is valid for the next 10 minutes. If you did not request a password reset, please disregard this email. Your account security is our top priority.

For any assistance, feel free to contact our support team.
'''

            # Send OTP via email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'OTP sent to your email.'})

        except UserDetails.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Email not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def verify_email_otp(request):
    if request.method == 'POST':
        try:
            otp_sent = request.session.get('otp')
            email = request.session.get('email')
            otp_time_str = request.session.get('otp_time')

            if not otp_sent or not otp_time_str:
                return JsonResponse({'success': False, 'message': 'No OTP found. Please request a new one.'})

            # Parse the ISO format string back to a datetime object
            otp_time = datetime.datetime.fromisoformat(otp_time_str)

            # Check if OTP is still valid (within 10 minutes)
            if timezone.now() > otp_time + datetime.timedelta(minutes=10):
                return JsonResponse({'success': False, 'message': 'OTP has expired. Please request a new one.'})

            data = json.loads(request.body)
            otp_provided = data.get('otp')

            if str(otp_provided) == str(otp_sent):
                return JsonResponse({'success': True, 'message': 'OTP verified successfully.', 'redirect_url': '/reset_password/'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid OTP. Please try again.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def reset_password_update(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'reset_password.html')

        email = request.session.get('email')
        if not email:
            messages.error(request, 'Session expired or email not found.')
            return render(request, 'reset_password.html')

        try:
            user = UserDetails.objects.get(user_email=email)
            user.user_password = make_password(new_password)
            user.save()

            messages.success(request, 'Your password has been reset successfully.')
            return HttpResponseRedirect('/login/')
        
        except UserDetails.DoesNotExist:
            msg = messages.error(request, 'User does not exist.')
            return render(request, 'reset_password.html', msg=msg)
    else:
        return render(request, 'reset_password.html')