# Generated by Django 4.2.3 on 2023-09-16 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_alter_fullanswer_date_responed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fulltask',
            name='category',
            field=models.CharField(default='general', max_length=200),
        ),
        migrations.AddField(
            model_name='fulltask',
            name='sub_category',
            field=models.CharField(default='other', max_length=200),
        ),
    ]
