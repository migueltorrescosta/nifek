# Generated by Django 4.1.4 on 2023-01-05 21:39

import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesis',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='content',
            field=models.TextField(unique=True),
        ),
    ]
