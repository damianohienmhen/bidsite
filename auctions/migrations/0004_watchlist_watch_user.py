# Generated by Django 3.1.2 on 2020-12-11 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_watchlist_watch_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='watch_user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='watchusers', to=settings.AUTH_USER_MODEL),
        ),
    ]
