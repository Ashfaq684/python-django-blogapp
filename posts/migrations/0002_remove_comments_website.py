# Generated by Django 5.0.1 on 2024-03-06 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='website',
        ),
    ]
