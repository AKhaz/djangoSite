# Generated by Django 3.1.6 on 2021-03-12 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0002_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
