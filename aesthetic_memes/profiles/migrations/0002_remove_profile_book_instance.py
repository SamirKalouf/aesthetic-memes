# Generated by Django 2.0.3 on 2018-03-29 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='book_instance',
        ),
    ]
