# Generated by Django 3.2.3 on 2022-03-31 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0020_session_follows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hearing',
            name='link',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='hearing',
            name='location',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='hearing',
            name='time',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
