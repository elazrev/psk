# Generated by Django 4.2.3 on 2023-07-16 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_invited_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='invited_by',
        ),
        migrations.AlterField(
            model_name='profile',
            name='invited_users',
            field=models.ManyToManyField(blank=True, to='users.profile'),
        ),
    ]
