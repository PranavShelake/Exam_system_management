# Generated by Django 5.1.2 on 2024-12-08 12:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_exam_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='group',
        ),
        migrations.RemoveField(
            model_name='subquestion',
            name='question',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='text',
            new_name='question_text',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='creator',
        ),
        migrations.AddField(
            model_name='exam',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='teacher.exam'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exam',
            name='instructions',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='QuestionGroup',
        ),
        migrations.DeleteModel(
            name='SubQuestion',
        ),
    ]
