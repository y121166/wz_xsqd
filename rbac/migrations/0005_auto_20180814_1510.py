# Generated by Django 2.1 on 2018-08-14 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_auto_20180814_1430'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='permission',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='role',
            old_name='name',
            new_name='title',
        ),
    ]
