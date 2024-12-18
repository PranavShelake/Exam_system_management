# Generated by Django 5.1.2 on 2024-12-10 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0008_teacher_email_teacher_first_name_teacher_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='email',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='password',
        ),
        migrations.AddField(
            model_name='teacher',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
