# Generated by Django 2.1.7 on 2019-08-27 05:35

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0007_auto_20190826_2220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'get_latest_by': 'last_modified'},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'get_latest_by': 'last_modified'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'get_latest_by': 'last_modified'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'get_latest_by': 'last_modified'},
        ),
        migrations.AddField(
            model_name='page',
            name='last_modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='block0',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='block1',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
