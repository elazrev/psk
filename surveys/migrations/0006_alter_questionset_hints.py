# Generated by Django 4.2.3 on 2023-07-23 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_alter_questionset_set_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='hints',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
