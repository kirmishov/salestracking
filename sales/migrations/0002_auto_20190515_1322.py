# Generated by Django 2.2.1 on 2019-05-15 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
