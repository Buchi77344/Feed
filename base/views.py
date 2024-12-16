from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import CustomUser
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth
# Create your views here.
def index(request):
    return render (request, 'index.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser  # Ensure this imports your custom user model

def signup(request):
    if request.method == "POST":
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        # Check if passwords match
        if password != password1:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        # Check if phone number already exists
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number already exists.')
            return redirect('signup')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        # Create the user
        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,  # Using email as username
            phone_number=phone_number,
            password=password,
        )
        user.save()

        # Success message and redirect to login
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('login')

    # Render the signup form
    return render(request, 'signup.html')


def login (request):
    if request.method == "POST":
        email = request.POST.get('email')
        password =request.POST.get('password')

        user = auth.authenticate(request, username=email,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')

        else:
            messages.error(request, 'invalid Credentials')
            return redirect('login')
    else:

       return render (request, 'login.html')


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.conf import settings

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from smtplib import SMTPException
from django.contrib.auth.models import User

def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"

            try:
                send_mail(
                    'Reset Your Password',
                    f"Hi {user.username},\n\nUse the link below to reset your password:\n{reset_link}\n\nIf you didn't request this, please ignore this email.",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'A password reset link has been sent to your email.')
            except SMTPException as e:
                messages.error(request, f"Email could not be sent. Error: {e}")
                return redirect('forget')

        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with this email.')
        except BadHeaderError:
            messages.error(request, 'Invalid header found in email.')

        return redirect('forget')
    return render(request, 'forget.html')

from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib import messages

CustomUser = get_user_model()

def reset_password(request, uidb64, token):
    try:
        # Decode the user ID from the URL
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (CustomUser.DoesNotExist, ValueError, TypeError):
        messages.error(request, "Invalid password reset link.")
        return redirect('forget')  # Redirect to "Forget Password" page

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and confirm_password:
            if new_password == confirm_password:
                # Validate the token
                if default_token_generator.check_token(user, token):
                    # Save the new password
                    user.password = make_password(new_password)
                    user.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect('login')  # Redirect to login page
                else:
                    messages.error(request, "The password reset link is invalid or has expired.")
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})
