# Generated by Django 3.2 on 2023-02-13 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_alter_tags_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tags',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
    ]
