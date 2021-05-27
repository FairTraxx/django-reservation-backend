
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Restaurant(models.Model):
    name = models.CharField(primary_key=True, max_length=250)
    opening_time = models.CharField(max_length=8)
    closing_time = models.CharField(max_length=8)


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    table_number = models.IntegerField(null=False)
    size = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)])


class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    people = models.IntegerField(null=False)
    booking_date_time_start = models.DateTimeField()
    booking_date_time_end = models.DateTimeField()