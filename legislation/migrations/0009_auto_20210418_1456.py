# Generated by Django 2.2.5 on 2021-04-18 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0008_hearing_letter_date_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='committee',
            name='responsible_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='legislation.Team'),
        ),
        migrations.AddField(
            model_name='supportletter',
            name='letter_date_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
