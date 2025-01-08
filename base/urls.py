from django.urls import path
from .views import *


urlpatterns = [
    path('',index,name="index"),
    path('login',login,name="login"),
    path('signup',signup,name="signup"),
    path('forget',forget,name="forget"),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('profile',profile,name="profile"),
    path('start_campaign/',start_campaign,name="start_campaign"),
    path('find_campaign',find_campaign,name="find_campaign"),
    path('about',about,name="about"),
    path('faq',faq,name="faq"),
    path('api/search/', search_campaigns, name='search_campaigns'),
    path('support',support,name="support"),
    path('details/<str:token>/',details,name="details"),
    path('preview/<str:token>/',preview,name="preview"),
    path('fee_payout',fee_payout,name="fee_payout"),
    path('create_campaign/',create_campaign,name="create_campaign"),
    path('edit_campaign/<str:token>/',edit_campaign,name="edit_campaign"),
    path('donate/<str:token>/', donate, name="donate"),
]


