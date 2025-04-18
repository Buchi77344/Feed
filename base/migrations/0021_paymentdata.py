# Generated by Django 5.0.1 on 2025-01-06 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_campaign_is_emergency'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paypal_secret_key', models.CharField(max_length=500)),
                ('paypal_api_key', models.CharField(max_length=500)),
                ('stripe_secret_key', models.CharField(max_length=500)),
                ('stripe_api_key', models.CharField(max_length=500)),
                ('currency', models.CharField(max_length=500)),
            ],
        ),
    ]
