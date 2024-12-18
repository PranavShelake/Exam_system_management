# Generated by Django 5.1.2 on 2024-12-10 11:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_studentanswer_answer_pdf'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('enrollment_number', models.CharField(max_length=100, unique=True)),
                ('course', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField()),
                ('teachers', models.ManyToManyField(related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='StudentAnswer',
        ),
    ]
