# Generated by Django 3.2.3 on 2021-05-26 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablebooking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='table_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]