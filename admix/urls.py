from django.urls import path
from admix.views import *

app_name="admix"
urlpatterns = [
    path('dashboard',dashboard,name='dashboard'),
    path('list_campaign',list_campaign,name='list_campaign'),
    path('emergency',emergency,name='emergency'),
    path('signup',signup,name='signup'),
    path('config',config,name='config'),
    path('login',login,name='login'),
    path('approve/<str:token>/',approve, name='approve'),
    path('delete/<str:token>/', delete_campaign, name='delete_campaign'),
    path('feature',feature,name='feature'),
    path('api/update-features/', update_features, name='update_features'),
    path('trending',trending,name='trending'),
    path('api/update-trend/', update_trend, name='update_trend'),
]

