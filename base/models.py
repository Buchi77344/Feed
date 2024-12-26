from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django_countries.fields import CountryField  


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
# Create your models here.
class Profile(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    # donation = models.ForeignKey("Donation",on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return  f"{self.user.username}"


def save_user_model(sender ,instance,created,**kwargs):
    if created:
          Profile.objects.create(user=instance) 
   

post_save.connect(save_user_model, sender=CustomUser ) 


class Campaign(models.Model):
    CATEGORY_CHOICES = [
        ('organisation/charity/npo/pbo', 'Organisation/Charity/NPO/PBO'),
        ('in loving memory of', 'In Loving Memory Of'),
        ('fire/drought/disaster/support', 'Fire/Drought/Disaster/Support'),
        ('education & training', 'Education & Training'),
        ('sport', 'sport'),
        ('Social welfare/commnity development/support', 'Social Welfare/Commnity Development/Support'),
        ('youth', 'youth'),
        ('arts & culture', 'Arts & Culture'),
        ('Nature conservation', 'Nature Conservation'),
        ('Animal Welfare/outreach', 'Animal Welfare/Outreach'),
        ('Vehicle', 'Vehicle'),
        ('Home', 'Home'),
        ('Business/App', 'Business/App'),
        ('legal', 'Legal'),
        ('Other', 'Other'),
    ]
    EVENT_CHOICE  = [
        ('aQuelle Midmar Mile 2025', 'aQuelle Midmar Mile 2025'),
        ('Hyrox johannesburg|Season 24/25', 'Hyrox johannesburg|Season 24/25'),
        ('vusa24', 'vusa24'),
        ('Comrades 2024', 'Comrades 2024'),
        ('WESEEYOU EVENT', 'WESEEYOU EVENT'),
        ('AMASHOVA DURBA CLASSIC', 'AMASHOVA DURBA CLASSIC'),
        ('IRONMAN 70.3 -2024', 'IRONMAN 70.3 -2024'),
        ('ANNUAL KIDS CHRISTMAS PARTY', 'ANNUAL KIDS CHRISTMAS PARTY'),
        ('aQuelle Midmar Mile 2025', 'aQuelle Midmar Mile 2025'),
    ]
    SECTOR_CHOICE = [ 
        ('child welfare','Child Welfare'),
        ('education','Education'),
        ('Community development','Community Development'),
        ('Environmental','Environmental'),
        ('Health','Health'),
        ('medical','Medical'),

    ]
    campaign_name = models.CharField( max_length=50)
    monetary = models.DecimalField( max_digits=15, decimal_places=2)
    category = models.CharField(max_length=100 , choices= CATEGORY_CHOICES)
    story = models.TextField()
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICE, null=True)
    event = models.CharField(max_length=100, choices=EVENT_CHOICE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='images/')
    video_url = models.URLField(max_length=1000 , blank=True)
    social_link  = models.URLField( max_length=1000, blank=True)
    address = models.CharField(max_length=100,null=True)
    address1 = models.CharField(max_length=100)
    city  = models.CharField( max_length=100)
    zipcode = models.CharField( max_length=50)
    state = models.CharField(max_length=50)
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    organization_payment = models.BooleanField(default=False)
    single_payment = models.BooleanField(default=False) 
    is_featured = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,blank=True,null=True)
    goal = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)



from decimal import Decimal 

class Donation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="donations")
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    message = models.TextField(blank=True, null=True)  # Optional message from the donor
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} donated {self.amount} to {self.campaign.campaign_name}"

class Newsletter(models.Model):
     email = models.EmailField( max_length=400)

     def __str__(self):
         return  f"{self.email}"  