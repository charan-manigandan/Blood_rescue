# Generated by Django 4.2.2 on 2024-02-18 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donors',
            name='age',
            field=models.BigIntegerField(),
        ),
    ]
