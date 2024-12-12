# Generated by Django 5.1.2 on 2024-12-08 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_remove_question_group_remove_subquestion_question_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='exam_time',
        ),
        migrations.AddField(
            model_name='exam',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]