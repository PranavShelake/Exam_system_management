# Generated by Django 5.1.2 on 2024-12-08 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_remove_exam_exam_time_exam_end_time_exam_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='exam_date',
        ),
    ]
