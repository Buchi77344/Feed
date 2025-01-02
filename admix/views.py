from django.shortcuts import render
from base.models import *

# Create your views here.
def dashboard(request):
    campaign_count =Campaign.objects.count()
    context ={
        'campaign_count':campaign_count
    }
    return render (request, 'admin/dashboard.html',context)

