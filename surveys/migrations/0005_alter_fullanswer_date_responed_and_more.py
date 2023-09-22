# Generated by Django 4.2.3 on 2023-09-16 12:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_alter_fulltask_category_alter_fulltask_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fullanswer',
            name='date_responed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fullanswer',
            name='date_sent',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='fulltask',
            name='sub_category',
            field=models.CharField(choices=[('survey', 'שאלון'), ('fill_in_the_blanks', 'השלמת משפטים'), ('text_or_image', 'רגשות מטקסט או תמונה')], default='survey', max_length=200),
        ),
    ]
