# Generated by Django 4.1.5 on 2023-01-16 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_remove_follow_following_follow_followed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='followed',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='follower',
        ),
        migrations.AddField(
            model_name='follow',
            name='followed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follow',
            name='following_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
