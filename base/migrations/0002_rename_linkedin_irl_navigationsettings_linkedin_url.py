# Generated by Django 5.1.5 on 2025-01-29 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='navigationsettings',
            old_name='linkedin_irl',
            new_name='linkedin_url',
        ),
    ]
