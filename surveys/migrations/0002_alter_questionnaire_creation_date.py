# Generated by Django 4.2.3 on 2023-07-22 17:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='creation_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
