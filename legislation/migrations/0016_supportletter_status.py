# Generated by Django 2.2.5 on 2021-04-28 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislation', '0015_auto_20210427_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportletter',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Unassigned'), (2, 'Assigned'), (3, 'Sent')], default=1),
        ),
    ]
