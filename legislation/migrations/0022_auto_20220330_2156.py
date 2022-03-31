# Generated by Django 3.2.3 on 2022-03-31 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0021_auto_20220330_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='committee',
            name='letter_days',
            field=models.IntegerField(default=7),
        ),
        migrations.AddField(
            model_name='committee',
            name='letter_time',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
