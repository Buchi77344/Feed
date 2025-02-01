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
        end_date__gte=datetime.now(),is_launch= True # Campaigns still active
    ).order_by('-monetary')[:3]

    campaigns = Campaign.objects.all()[:3]
    campaigns_with_percentage = []
    campaigns_with_percentages = []
    # if Campaign.objects.filter(profile__user =request.user).exists: 
    for campaign in featured_campaigns:
        # Calculate total donations for the campaign
       
        total_donations = campaign.donations.aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate percentage achieved
        percentage_achieved = (total_donations / campaign.monetary) * 100 if campaign.monetary > 0 else 0

        # Add campaign data and percentage to the list
        campaigns_with_percentage.append({
            'campaign': campaign,
            'total_donations': total_donations,
            'percentage_achieved': percentage_achieved,
            'trending_campaigns':trending_campaigns,
        })
    for campaign in campaigns:
        # Calculate total donations for the campaign
       
        total_donations = campaign.donations.aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate percentage achieved
        percentage_achieved = (total_donations / campaign.monetary) * 100 if campaign.monetary > 0 else 0

        # Add campaign data and percentage to the list
        campaigns_with_percentages.append({
            'campaign': campaign,
            'total_donations': total_donations,
            'percentage_achieved': percentage_achieved,
            'trending_campaigns':trending_campaigns,
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
            messages.success(request, 'email added sucessfully')
            return redirect('/')
    if SocialMedia.objects.exists():
        social = get_object_or_404(SocialMedia)
    campaign = Campaign.objects.all()

 

    for campaign in campaign :
        last =  Donation.objects.filter(campaign=campaign).order_by('-created_at').first()
        
 
    
    context = {
        'featured_campaigns': featured_campaigns,
        'campaigns':campaigns, 
        'trending_campaigns': trending_campaigns,
        'campaigns_with_percentage':campaigns_with_percentage,
        'campaigns_with_percentages':campaigns_with_percentages,
        'social':social,
        'last':last,
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
            messages.success(request, 'login sucessfully')
            return redirect('/')

        else:
            messages.error(request, 'invalid Credentials')
            return redirect('login')
    else:

       return render (request, 'login.html')
    

def logout(request):
    auth.logout(request)
    messages.success(request, 'you have sucessfully logout')
    return redirect('login')


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


from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Campaign
from django_countries import countries

@login_required(login_url="login")
def start_campaign(request):
    if request.method == 'POST':
        try:
            # Extract data directly from request.POST and request.FILES
            campaign_name = request.POST.get('campaign_name')
            monetary = request.POST.get('monetary')
            category = request.POST.get('category')
            story = request.POST.get('story')
            event = request.POST.get('event') 
            images = request.FILES.get('images')
            video_url = request.POST.get('video_url')
            social_link = request.POST.get('social_link')
            address = request.POST.get('address')
            address1 = request.POST.get('address1')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            
            # Check if 'is_emergency' checkbox is checked (True) or not (False)
            is_emergency = 'is_emergency' in request.POST

            # Validate required fields here, for example:
            # if not all([campaign_name, monetary, category, story, event, start_date, end_date]):
            #     raise ValueError("Please fill in all required fields.")

            # Create and save the campaign object
            campaign = Campaign.objects.create(
                campaign_name=campaign_name,
                monetary=monetary,
                category=category,
                story=story,
                event=event,
                images=images,
                video_url=video_url,
                social_link=social_link,
                address=address,
                address1=address1,
                city=city,
                state=state, 
                country=country,
                start_date=start_date,
                end_date=end_date, 
                user=request.user,
                is_status=True,
                is_emergency=is_emergency  # Directly set the boolean value for is_emergency
            )

            # Return the created campaign's token as JSON response
            return redirect ('profile')

        except Exception as e:
            category = Campaign.CATEGORY_CHOICES
            event = Campaign.EVENT_CHOICE
            messages.error(request, f"Error creating campaign: {str(e)}")
          
            return redirect ('start_campaign')

    # Define category and event choices
  
    category = Campaign.CATEGORY_CHOICES
    event = Campaign.EVENT_CHOICE

    # You need to define the 'countries' variable, either from a model
  # Example list, replace with actual dataz
    if SocialMedia.objects.exists():
        social = get_object_or_404(SocialMedia)
    
    context = {
        'countries': countries,
        'category': category,
        'event': event,
        'social':social
    }

    return render(request, 'start_campaign.html', context)


from django.http import JsonResponse
from django.shortcuts import render
from .models import Campaign

@login_required(login_url="login")
def create_campaign(request):
    if request.method == 'POST':
        # Get data from the request
        campaign_name = request.POST.get('campaign_name')
        monetary = request.POST.get('monetary')
        category = request.POST.get('category')
        story = request.POST.get('story')
        event = request.POST.get('event')
        images = request.FILES.get('images')  # Handle image upload
        video_url = request.POST.get('video_url')
        social_link = request.POST.get('social_link')
        address = request.POST.get('address')
        address1 = request.POST.get('address1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Create and save the Campaign object
        campaign = Campaign.objects.create(
            campaign_name=campaign_name,
            monetary=monetary,
            category=category,
            story=story,
            event=event,
            images=images,
            video_url=video_url,
            social_link=social_link,
            address=address,
            address1=address1,
            city=city,
            state=state,
            country=country,
            start_date=start_date,
            end_date=end_date,
            user =request.user
        )
        print('id', campaign.token)
        # Return JSON response with the ID of the newly created campaign
        return JsonResponse({'id': campaign.token})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
from django.shortcuts import render, get_object_or_404
from .models import Campaign

@login_required(login_url="login")
def edit_campaign(request,token):
    # Retrieve the campaign object by its ID
    campaign = get_object_or_404(Campaign, token=token)
    
    if request.method == 'POST':
        # Handle form submission for updating the campaign
        campaign.campaign_name = request.POST.get('campaign_name')
        campaign.monetary = request.POST.get('monetary')
        campaign.category = request.POST.get('category')
        campaign.story = request.POST.get('story')
        campaign.event = request.POST.get('event')
        campaign.images = request.FILES.get('images', campaign.images)  # Keep existing if no new image
        campaign.video_url = request.POST.get('video_url')
        campaign.social_link = request.POST.get('social_link')
        campaign.address = request.POST.get('address')
        campaign.address1 = request.POST.get('address1')
        campaign.city = request.POST.get('city')
        campaign.state = request.POST.get('state')
        campaign.country = request.POST.get('country')
        campaign.start_date = request.POST.get('start_date')
        campaign.end_date = request.POST.get('end_date')
        campaign.save()
        return JsonResponse({'token': campaign.token})
    
    # Render the form pre-filled with the campaign's data
    category = Campaign.CATEGORY_CHOICES
    event =Campaign.EVENT_CHOICE
    return render(request, 'edit_campaign.html', {'campaign': campaign, 'countries':countries, 'category':category,
        'event':event,})


from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Campaign, Donation, Profile

@login_required(login_url="login")
def profile(request):
    # Fetch the user's campaigns, limiting to the first 2
    campaigns = Campaign.objects.filter(user=request.user)[:2]
    
    # Fetch the user's profile
    profile = get_object_or_404(Profile, user=request.user)
    
    # Get all donations associated with campaigns created by this user
    donations = Donation.objects.filter(campaign__user=request.user).select_related("campaign", "user")
    
    # Calculate total donations for each campaign and update the campaign's goal
    for campaign in campaigns:
        total_donations = campaign.donations.aggregate(total=Sum('amount'))['total'] or 0
        campaign.goal = total_donations  # Assuming 'goal' represents total donations here
        campaign.save()

    if request.method == "POST":
        # Extract form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        address = request.POST.get('address', '').strip()
        
        # Update user information
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Update profile information
        profile.address = address
        profile.save()
        
        return redirect('profile')  # Redirect to the profile page after saving

    # Context to pass to the template
    if SocialMedia.objects.exists():
        social = get_object_or_404(SocialMedia)
    context = {
        "campaigns": campaigns,
        "donations": donations,
        "profile": profile,
        "social": social
    }
    return render(request, 'profile.html', context)



from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="login")
def donate(request, token):
    campaign = get_object_or_404(Campaign, token=token)
  
            

           
    if SocialMedia.objects.exists():
        social = get_object_or_404(SocialMedia)
    context ={
            'campaign':campaign,
            'social':social
        }
    return render(request, 'donate.html',context)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal
from paypalrestsdk import Payment
import paypalrestsdk
import logging
from .models import PaymentData
if  PaymentData.objects.all().exists():

   data = get_object_or_404(PaymentData)

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": "",
    "client_secret": "",
})

from django.http import JsonResponse
from decimal import Decimal
import logging

from paypalrestsdk import Payment
import json

from decimal import Decimal
import json
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Campaign
from paypalrestsdk import Payment

def paypal_payment_link(request, token):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=400)

    # Get the campaign object based on the token
    campaign = get_object_or_404(Campaign, token=token)

    try:
        # Parse the request body as JSON
        data = json.loads(request.body)

        # Extract and validate the amount
        amount_str = data.get('amount')
        if not amount_str:
            return JsonResponse({"error": "Donation amount is required."}, status=400)
        
        try:
            amount = Decimal(amount_str)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid donation amount."}, status=400)

        if amount <= 0:
            return JsonResponse({"error": "Donation amount must be greater than zero."}, status=400)

        # Extract optional message
        message = data.get('message', '')

        # Create a PayPal payment
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": f"{amount:.2f}",
                    "currency": "USD"
                },
                "description": f"Donation to {campaign.campaign_name}"
            }],
            "redirect_urls": {
                "return_url": request.build_absolute_uri(
                    f"/paypal-success/{token}/?amount={amount}&message={message}"
                ),
                "cancel_url": request.build_absolute_uri(f"/paypal-cancel/{token}/")
            }
        })

        # Attempt to create the payment
        if payment.create():
            approval_url = next((link.href for link in payment.links if link.rel == "approval_url"), None)
            if approval_url:
                return JsonResponse({
                    "success": True,
                    "approval_url": approval_url,
                    "campaign_token": campaign.token  # Dynamically include the campaign token
                })
            else:
                return JsonResponse({"error": "Approval URL not found in PayPal response."}, status=500)
        else:
            logging.error(payment.error)
            return JsonResponse({"error": "Unable to create PayPal payment. Check the logs for more details."}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data in the request body."}, status=400)
    except Exception as e:
        logging.exception("An error occurred while processing the payment request.")
        return JsonResponse({"error": str(e)}, status=400)


import json
import logging
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Campaign
import stripe

# Set your Stripe secret key
stripe.api_key = "your_stripe_secret_key"

def stripe_payment_link(request, token):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=400)

    # Get the campaign object based on the token
    campaign = get_object_or_404(Campaign, token=token)

    try:
        # Parse the request body as JSON
        data = json.loads(request.body)

        # Extract and validate the amount
        amount_str = data.get('amount')
        if not amount_str:
            return JsonResponse({"error": "Donation amount is required."}, status=400)

        try:
            amount = Decimal(amount_str)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid donation amount."}, status=400)

        if amount <= 0:
            return JsonResponse({"error": "Donation amount must be greater than zero."}, status=400)

        # Convert amount to cents (Stripe processes amounts in the smallest currency unit)
        amount_in_cents = int(amount * 100)

        # Extract optional message
        message = data.get('message', '')

        # Create a Stripe PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency="usd",
            description=f"Donation to {campaign.campaign_name}",
            metadata={
                "campaign_name": campaign.campaign_name,
                "message": message,
            },
        )

        # Return the client secret for the PaymentIntent
        return JsonResponse({
            "success": True,
            "client_secret": payment_intent.client_secret,
            "campaign_token": campaign.token
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data in the request body."}, status=400)
    except stripe.error.StripeError as e:
        logging.error(f"Stripe error: {e.user_message}")
        return JsonResponse({"error": f"Stripe error: {e.user_message}"}, status=400)
    except Exception as e:
        logging.exception("An error occurred while processing the payment request.")
        return JsonResponse({"error": str(e)}, status=400)




def find_campaign(request):
    campaigns = Campaign.objects.filter(is_launch=True)
    campaigns_with_percentage = []
   
    for campaign in campaigns:
        # Calculate total donations for the campaign
        total_donations = campaign.donations.aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate percentage achieved
        percentage_achieved = (total_donations / campaign.monetary) * 100 if campaign.monetary > 0 else 0

        # Add campaign data and percentage to the list
        campaigns_with_percentage.append({
            'campaign': campaign,
            'total_donations': total_donations,
            'percentage_achieved': percentage_achieved,
        })
    if SocialMedia.objects.exists():
        social = get_object_or_404(SocialMedia)
    context ={
            'campaigns_with_percentage':campaigns_with_percentage,
            'social':social
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




from django.shortcuts import get_object_or_404, render
from django.db.models import Sum ,Count
from decimal import Decimal  # Import Decimal for correct type handling

def details(request, token):
    # Get the specific campaign
    campaign_details = get_object_or_404(Campaign, token=token)

    # Get all donations related to this campaign
    donation = Donation.objects.filter(campaign=campaign_details)

    # Calculate total donations for this campaign
    total_donations = donation.aggregate(total=Sum('amount'))['total'] or Decimal(0)

    # Update the campaign's goal with the total donations (if applicable)
    campaign_details.goal = total_donations
    campaign_details.save()

    # Ensure both values are Decimal before performing division
    if campaign_details.monetary > 0:
        percentage_achieved = (total_donations / campaign_details.monetary) * Decimal(100)
    else:
        percentage_achieved = Decimal(0)

    # Pass the campaign details and percentage to the template
    campaign_with_donations= get_object_or_404(Campaign.objects.annotate(total_donations =Count('donations')),token=token)
    

    context = {
        'campaign_details': campaign_details,
        'total_donations': total_donations,
        'percentage_achieved': percentage_achieved,
        'donation': donation,
        'campaign_with_donations':campaign_with_donations
    }
    return render(request, 'details.html', context)




@login_required(login_url="login")
def preview(request,token):
    campaign_details = get_object_or_404(Campaign,token=token )
    context ={
        'campaign_details':campaign_details,
        
    }
    return render (request, 'preview.html',context)

def fee_payout(request):
    return render (request,'feeds-payout.html')








