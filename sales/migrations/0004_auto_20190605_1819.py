# Generated by Django 2.2.1 on 2019-06-05 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20190605_1801'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='id',
            new_name='ref_id',
        ),
    ]