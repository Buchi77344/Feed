from django.urls import path
from .views import *


urlpatterns = [
    path('',index,name="index"),
    path('login',login,name="login"),
    path('signup',signup,name="signup"),
    path('forget',forget,name="forget"),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('profile',profile,name="profile"),
    path('start_campaign',start_campaign,name="start_campaign"),
]


