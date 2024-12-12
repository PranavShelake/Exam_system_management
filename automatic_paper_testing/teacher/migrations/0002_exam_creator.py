# Generated by Django 5.1.2 on 2024-12-08 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='creator',
            field=models.ForeignKey(blank=True, help_text='The teacher who created this exam paper', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_exams', to=settings.AUTH_USER_MODEL),
        ),
    ]
