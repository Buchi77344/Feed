from django.shortcuts import render ,get_object_or_404 ,redirect
from base.models import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages ,auth


# Create your views here.
@login_required(login_url='admix:login')
def dashboard(request):
    campaign_count =Campaign.objects.count()
    active_campaign = Campaign.objects.filter(is_launch= True).count()
    pending_campaign = Campaign.objects.filter(is_launch= False).count()
    total = Donation.objects.aggregate(total_amount=Sum('amount'))['total_amount'] 
    total = total if total else 0
    campaign = Campaign.objects.all().order_by('-start_date')[:3]
    
    context ={
        'campaign_count':campaign_count,
        'active_campaign':active_campaign,
        'pending_campaign':pending_campaign,
        'total':total,
        'campaign':campaign
    }
    return render (request, 'admin/dashboard.html',context)

@login_required(login_url='admix:login')
def list_campaign(request):
  
    campaign = Campaign.objects.all()
         

    context ={
            'campaign':campaign
        }
    return render (request, 'admin/admin-campaign.html',context)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from base.models import Campaign
import json

@csrf_exempt
def approve(request, token):
    if request.method == "POST":
        try:
            # Parse the request data
            data = json.loads(request.body)
            is_status = data.get('value', True)

            # Use get_or_create to either get an existing campaign or create a new one
            campaign, created = Campaign.objects.get_or_create(token=token)

            # Update the status regardless of whether the campaign was created or fetched
            campaign.is_launch = True
            campaign.save()

            # Return a successful response with the updated status
            return JsonResponse({'status': True}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid HTTP method'}, status=405)

@login_required(login_url='admix:login')
def emergency(request):
  
    campaign = Campaign.objects.filter(is_emergency=True)

         

    context ={
            'campaign':campaign
        }
    return render (request, 'admin/emergency.html',context)

def signup(request):
    if request.method == "POST":
        # Retrieve form data
      
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        # Check if passwords match
        if password != password1:
            messages.error(request, 'Passwords do not match.')
            return redirect(' admix:signup')

        # Check if phone number already exists
        

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('admix:signup')

        # Create the user
        user = CustomUser.objects.create_user(
            username=email,
            email=email,  # Using email as username
            phone_number=phone_number,
            password=password,
            is_staff =True
        )
        user.save()

        # Success message and redirect to login
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('admix:login')

    # Render the signup form
    return render(request, 'admin/signup.html')


def login (request):

    if request.method == "POST":
        email = request.POST.get('email')
        password =request.POST.get('password')

        user = auth.authenticate(request, username=email,password=password)

        if user is not None :
            if user.is_staff:

               auth.login(request,user)
               return redirect('admix:dashboard')  
            else:
                 messages.error(request, 'You do not have Admin access')
                 return redirect('admix:login')
    

        else:
            messages.error(request, 'invalid Credentials')
            return redirect('admix:login')
    else:

       return render (request, 'admin/login/login.html')
    


def config(request): 
    if request.method == "POST":
        # Correct the typo `POT` to `POST`
        paypal_secret_key = request.POST.get('paypal_secret_key')
        paypal_api_key = request.POST.get('paypal_api_key')
        stripe_secret_key = request.POST.get('stripe_secret_key')
        stripe_api_key = request.POST.get('stripe_api_key')
        currency = request.POST.get('currency')

        # Save or create the PaymentData object
        configure, created = PaymentData.objects.get_or_create(
            paypal_secret_key=paypal_secret_key,
            paypal_api_key=paypal_api_key,
            stripe_secret_key=stripe_secret_key,
            stripe_api_key=stripe_api_key,
            currency=currency
        )
        configure.save()
        return redirect("admix:config") 

    # Fetch the first PaymentData object or set context values to None
    if PaymentData.objects.exists():
        pay = PaymentData.objects.first()
        context = {
            'paypal_secret_key': pay.paypal_secret_key,
            'paypal_api_key': pay.paypal_api_key,
            'stripe_secret_key': pay.stripe_secret_key,
            'stripe_api_key': pay.stripe_api_key,
            'currency': pay.currency,
        }
    else:
 
        context = {
            'paypal_secret_key': 'Enter PayPal Secret Key',
            'paypal_api_key': 'Enter PayPal API Key',
            'stripe_secret_key': 'Enter Stripe Secret Key',
            'stripe_api_key': 'Enter Stripe API Key',
            'currency': 'currency',
        }

   
    return render(request, 'admin/set.html', context)

def social(request):
    social ,created = SocialMedia.objects.get_or_create(id=1)
    if request.method == "POST":
        social.whatsapp =request.POST.get('whatsapp',social.whatsapp)
        social.telegram =request.POST.get('telegram',social.telegram)
        social.linkdin =request.POST.get('linkdin',social.linkdin)
        social.twitter =request.POST.get('twitter',social.twitter)
        social.instagram =request.POST.get('instagram',social.instagram)
        social.facebook =request.POST.get('facebook',social.facebook)
        social.tiktok =request.POST.get('tiktok',social.tiktok)
        social.youtube =request.POST.get('youtube',social.youtube)

     
       
        social.save()
        return redirect("admix:social") 
    if  SocialMedia.objects.exists():
            social = SocialMedia.objects.first()
            context = {
                'whatsapp':social.whatsapp,
                'telegram' :social.telegram,
                'linkdin':social.linkdin,
                'twitter':social.twitter,
                'instagram':social.instagram,
                'facebook':social.facebook,
                'tiktok':social.tiktok,
                'youtube':social.youtube,
            }
    else:
            context = {
            'whatsapp': 'Enter Your Whatsapp Link',
            'telegram': 'Enter Your telegram Link',
             'linkdin': 'Enter Your linkedin Link',
            'twitter': 'Enter Your Twitter Link',
            'instagram': 'Enter Your Instagram Link',
            'facebook': 'Enter Your Facebook Link',
            'tiktok': 'Enter Your Tiktok Link',
            'youtube': 'Enter Your Youtube Link',
            }
       

    return render (request, 'admin/social.html',context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
  # Replace with your actual model

@csrf_exempt
def delete_campaign(request, token):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, token=token)
        campaign.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)


def feature(request):
    feature = Campaign.objects.all()
    context = {
        'feature':feature
    }
    return render (request,  'admin/feature.html',context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



@csrf_exempt
def update_features(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            features = data.get("features", [])

            # Iterate over the selected features
            for feature in features:
                feature_id = feature.get("id")

                # Update the Campaign object based on the feature ID
                if feature_id:
                    # Assuming 'Feature' is related to 'Campaign' and 'id' is the primary key for features
                    # Here you are updating the corresponding campaign with is_featured=True
                    Campaign.objects.filter(id=feature_id).update(is_featured=True)

            return JsonResponse({"message": "Features updated successfully!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def update_trend(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            features = data.get("features", [])

            # Iterate over the selected features
            for feature in features:
                feature_id = feature.get("id")

                # Update the Campaign object based on the feature ID
                if feature_id:
                    # Assuming 'Feature' is related to 'Campaign' and 'id' is the primary key for features
                    # Here you are updating the corresponding campaign with is_featured=True
                    Campaign.objects.filter(id=feature_id).update(is_trending=True)

            return JsonResponse({"message": "Trending Campaign updated successfully!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def trending(request):
    feature = Campaign.objects.all()
    context = {
        'feature':feature
    }
    return render (request,  'admin/trending.html',context)