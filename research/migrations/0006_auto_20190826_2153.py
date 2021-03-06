# Generated by Django 2.1.7 on 2019-08-27 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0005_auto_20190310_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homepage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='last_modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='last_modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='person',
            name='last_modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='project',
            name='last_modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='research.Person'),
        ),
    ]
