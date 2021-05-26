# Generated by Django 3.2.3 on 2021-05-26 11:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('name', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('opening_time', models.CharField(max_length=8)),
                ('closing_time', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(null=True)),
                ('size', models.IntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tablebooking.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people', models.IntegerField()),
                ('booking_date_time_start', models.DateTimeField()),
                ('booking_date_time_end', models.DateTimeField()),
                ('time_slots', models.PositiveSmallIntegerField(choices=[(1, '12:00PM to 3:00PM'), (2, '3:00PM to 6:00PM'), (3, '6:00PM to 9:00PM'), (4, '9:00PM to 11:59PM')], default=1)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tablebooking.table')),
            ],
        ),
    ]
