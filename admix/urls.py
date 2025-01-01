from django.urls import path
from admix.views import *

app_name="admix"
urlpatterns = [
    path('dashboard',dashboard,name='dashboard')
]
