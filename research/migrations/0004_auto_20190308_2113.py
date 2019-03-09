# Generated by Django 2.1.7 on 2019-03-09 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0003_project_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='authors',
            field=models.ManyToManyField(related_name='paper_authors', through='research.AuthorOrder', to='research.Person'),
        ),
    ]
