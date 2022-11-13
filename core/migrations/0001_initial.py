# Generated by Django 4.1.3 on 2022-11-07 22:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=20)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'properties',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='theses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'theses',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('deleted_on', models.DateTimeField(blank=True, default=None, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tags', to='core.property')),
                ('tagger', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tags', to=settings.AUTH_USER_MODEL)),
                ('thesis', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tags', to='core.thesis')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
