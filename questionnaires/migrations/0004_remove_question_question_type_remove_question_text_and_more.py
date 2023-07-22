# Generated by Django 4.2.3 on 2023-07-21 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questionnaires', '0003_remove_scalingquestion_question_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_type',
        ),
        migrations.RemoveField(
            model_name='question',
            name='text',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='interviewer',
        ),
        migrations.AddField(
            model_name='question',
            name='question_text',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='questionfile',
            name='explanation',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='questionfile',
            name='title',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='date_of_creation',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='explanation',
            field=models.TextField(default=''),
        ),
    ]
