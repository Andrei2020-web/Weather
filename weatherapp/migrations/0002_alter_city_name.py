# Generated by Django 4.1 on 2022-09-19 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.TextField(default='', max_length=50),
        ),
    ]
