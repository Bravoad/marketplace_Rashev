# Generated by Django 3.2 on 2023-02-01 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20230131_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='middle_name',
        ),
    ]
