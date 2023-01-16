# Generated by Django 4.1.5 on 2023-01-14 00:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cram', '0003_rename_success_card_success_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='starred_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='starred_collections', to=settings.AUTH_USER_MODEL),
        ),
    ]
