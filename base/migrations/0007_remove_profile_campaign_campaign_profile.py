# Generated by Django 5.0.1 on 2024-12-23 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_campaign_social_link_alter_campaign_video_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='campaign',
        ),
        migrations.AddField(
            model_name='campaign',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.profile'),
        ),
    ]