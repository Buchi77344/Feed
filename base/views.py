from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import CustomUser
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth
from  base.models  import *
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    featured_campaigns = Campaign.objects.filter(is_featured=True)[:3]
    
    # Trending Campaigns: Define based on most recent or highest monetary goal
    trending_campaigns = Campaign.objects.filter(
        end_date__gte=datetime.now()  # Campaigns still active
    ).order_by('-monetary')[:3]

    campaigns = Campaign.objects.all()
    campaigns_with_percentage = []
    # if Campaign.objects.filter(profile__user =request.user).exists: 
    for campaign in campaigns:
        # Calculate total donations for the campaign
        total_donations = campaign.donations.aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate percentage achieved
        percentage_achieved = (total_donations / campaign.goal) * 100 if campaign.goal > 0 else 0

        # Add campaign data and percentage to the list
        campaigns_with_percentage.append({
            'campaign': campaign,
            'total_donations': total_donations,
            'percentage_achieved': percentage_achieved,
        })
    
    # Calculate the percentage achieved
    
        percentage_achieved = (total_donations / campaign.goal) * 100 if campaign.goal > 0 else 0
    if request.method == "POST":
        email = request.POST.get('email')
        if Newsletter.objects.filter(email=email).exists():
            messages.error(request, 'email already exist')
            return redirect('index')
        else:
            Newsletter.objects.get_or_create(email=email)
            messages.error(request, 'email added sucessfully')
            return redirect('/')
    context = {
        'featured_campaigns': featured_campaigns,
        'campaigns':campaigns, 
        'trending_campaigns': trending_campaigns,
        'campaigns_with_percentage':campaigns_with_percentage,
    }
    return render (request, 'index.html',context)

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


# def start_campaign(request):
#     if request.method == "POST":
#         campaign_name = request.POST.get('campaign_name')
#         monetary = request.POST.get('monetary')
#         category = request.POST.get('category')
#         story = request.POST.get('story')
#         event = request.POST.get('event')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         video_url = request.POST.get('video_url')
#         social_link = request.POST.get('social_link')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         country = request.POST.get('country')
#         organization_payment = request.POST.get('organization_payment')
#         single_payment = request.POST.get('single_payment')

#     return render (request, 'start_campaign.html')

from django.contrib import messages
from .models import Campaign
from datetime import datetime

@login_required(login_url="login")
def start_campaign(request):
    if request.method == 'POST':
        try:
            # Extract data directly from request.POST and request.FILES
            campaign_name = request.POST.get('campaign_name')
            monetary = request.POST.get('monetary')
            category = request.POST.get('category')
            story = request.POST.get('story')
            sector = request.POST.get('sector')
            event = request.POST.get('event')
            image = request.FILES.get('image')
            video_url = request.POST.get('video_url')
            social_link = request.POST.get('social_link')
            address = request.POST.get('address')
            address1 = request.POST.get('address1')
            city = request.POST.get('city')
            zipcode = request.POST.get('zipcode')
            state = request.POST.get('state')
            country = request.POST.get('country')
            organization_payment = request.POST.get('organization_payment') == 'on'
            single_payment = request.POST.get('single_payment') == 'on'
            is_featured = request.POST.get('is_featured') == 'on'

            # Create and save the campaign object
            campaign = Campaign.objects.create(
                campaign_name=campaign_name,
                monetary=monetary,
                category=category,
                story=story,
                sector=sector,
                event=event,
                images=image,
                video_url=video_url,
                social_link=social_link,
                address=address,
                address1=address1,
                city=city,
                zipcode=zipcode,
                state=state,
                country=country,
                organization_payment=organization_payment,
                single_payment=single_payment,
                is_featured=is_featured,
                start_date=datetime.now(),
                end_date=datetime.now(),  # Update as needed
            )
            # profile = Profile.objects.get(user=request.user)
            # profile.campaign = campaign
            # profile.save()
            messages.success(request, f'Campaign "{campaign_name}" created successfully!')
            return redirect('profile')  # Adjust redirect as needed

        except Exception as e:
            messages.error(request, f"Error creating campaign: {str(e)}")
            return render(request, 'start_campaign.html', status=400)

    return render(request, 'start_campaign.html')
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def profile(request):
    campaign =  Campaign.objects.filter(profile__user=request.user)
    profile = get_object_or_404(Profile, user=request.user)

    # Get all donations for campaigns created by this profile
    donations = Donation.objects.filter(campaign__profile=profile).select_related("campaign", "user")
    context = {
        "campaign":campaign,
        "donations":donations,
        "profile":profile
    }
    return render (request, 'profile.html',context)


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def donate_to_campaign(request, campaign_id):
    if request.method == 'POST':
        campaign = get_object_or_404(campaign, id=campaign_id)
        amount = request.POST.get('amount')
        message = request.POST.get('message', '')

        try:
            amount = Decimal(amount)  # Validate and convert the amount
            if amount <= 0:
                raise ValueError("Donation amount must be greater than zero.")

            # Create a new donation
            Donation.objects.create(
                user=request.user,
                campaign=campaign,
                amount=amount,
                message=message
            )

            messages.success(request, f"Thank you for donating {amount} to {campaign.campaign_name}!")
            return redirect('campaign_detail', campaign_id=campaign.id)

        except Exception as e:
            messages.error(request, f"Error processing donation: {e}")
            return redirect('campaign_detail', campaign_id=campaign.id)

    return redirect('campaign_detail', campaign_id=campaign_id)


@login_required(login_url="login")
def find_campaign(request):
    campaigns = Campaign.objects.all()
    campaigns_with_percentage = []
    if Campaign.objects.filter(profile__user =request.user).exists: 
      for campaign in campaigns:
        # Calculate total donations for the campaign
        total_donations = campaign.donations.aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate percentage achieved
        percentage_achieved = (total_donations / campaign.goal) * 100 if campaign.goal > 0 else 0

        # Add campaign data and percentage to the list
        campaigns_with_percentage.append({
            'campaign': campaign,
            'total_donations': total_donations,
            'percentage_achieved': percentage_achieved,
        })
    context ={
            'campaigns_with_percentage':campaigns_with_percentage,
        }
    return render (request, 'find_campaign.html',context)

def about(request):
    return render (request, 'about.html')
def faq(request):
    return render (request, 'faq.html')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Campaign  # Assuming your model is named Campaign

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def search_campaigns(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            keyword = data.get('keyword', '')
            categories = data.get('categories', [])
            sectors = data.get('sectors', [])

            # Validate input 
            if not keyword and not categories and not sectors:
                return JsonResponse([], safe=False)

            # Query campaigns
            campaigns = Campaign.objects.all()

            if keyword:
                campaigns = campaigns.filter(campaign_name__icontains=keyword)
            # if keyword:
            #     campaigns = campaigns.filter(country__icontains=keyword)
            if categories:
                campaigns = campaigns.filter(category__in=categories)
            if sectors:
                campaigns = campaigns.filter(sector__in=sectors)

            results = list(campaigns.values(
                'campaign_name', 'country', 'story', 'category', 'sector', 'start_date', 'end_date'
            ))

            return JsonResponse(results, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=400)


def support(request):
    return render (request, 'support.html')
 