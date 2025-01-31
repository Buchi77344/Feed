from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Campaign)
admin.site.register(Donation)
admin.site.register(Newsletter)
admin.site.register(PaymentData)
admin.site.register(SocialMedia)
