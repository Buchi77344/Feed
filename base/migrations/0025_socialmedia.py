# Generated by Django 5.0.1 on 2025-01-31 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_campaign_is_trending'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp', models.CharField(max_length=300)),
                ('telegram', models.CharField(max_length=300)),
                ('linkdin', models.CharField(max_length=300)),
                ('twitter', models.CharField(max_length=300)),
                ('instagram', models.CharField(max_length=300)),
                ('facebook', models.CharField(max_length=300)),
                ('tiktok', models.CharField(max_length=300)),
                ('youtube', models.CharField(max_length=300)),
            ],
        ),
    ]
