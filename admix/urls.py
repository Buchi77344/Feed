from django.urls import path
from admix.views import *

app_name="admix"
urlpatterns = [
    path('dashboard',dashboard,name='dashboard'),
    path('list_campaign',list_campaign,name='list_campaign'),
    path('approve/<str:token>/',approve, name='approve')
]
