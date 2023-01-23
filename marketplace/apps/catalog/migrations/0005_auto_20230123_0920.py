# Generated by Django 3.2 on 2023-01-23 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_category_parent_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('value', models.CharField(max_length=250, verbose_name='Значение')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
        migrations.AddField(
            model_name='attributes',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.product'),
        ),
    ]
