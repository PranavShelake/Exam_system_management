# Generated by Django 5.1.2 on 2024-12-10 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_delete_studentanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='security_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
