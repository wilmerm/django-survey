# Generated by Django 5.0.4 on 2024-05-05 07:05

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('options_cssclass', models.CharField(default='col-sm-6 col-md-4 col-lg-3 col-xl-2', max_length=500)),
                ('create_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('vote_count', models.PositiveIntegerField(default=0, editable=False)),
                ('vote_percentage', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=5)),
                ('image', models.ImageField(blank=True, null=True, upload_to='survey/')),
                ('color', models.CharField(default='#FFFFFF', max_length=25)),
                ('create_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='survey.survey')),
                ('update_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('create_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_choices', to=settings.AUTH_USER_MODEL)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='survey.surveyoption')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
