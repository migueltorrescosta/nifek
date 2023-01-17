# Generated by Django 4.1.5 on 2023-01-17 01:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cram', '0005_alter_card_options_card_created_on_card_updated_on_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='owner',
        ),
        migrations.AlterUniqueTogether(
            name='usercardscore',
            unique_together={('user', 'card')},
        ),
    ]
