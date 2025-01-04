from django.shortcuts import render ,get_object_or_404
from base.models import *


# Create your views here.
def dashboard(request):
    campaign_count =Campaign.objects.count()
    context ={
        'campaign_count':campaign_count
    }
    return render (request, 'admin/dashboard.html',context)

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
