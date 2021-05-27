
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Restaurant(models.Model):
    name = models.CharField(primary_key=True, max_length=250)
    opening_time = models.CharField(max_length=8)
    closing_time = models.CharField(max_length=8)


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    table_number = models.IntegerField(null=False, unique=True)
    size = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)])
    def __str__(self):
        return str(self.table_number)


class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    people = models.IntegerField(null=False)
    booking_date_time_start = models.DateTimeField(unique=True)
    booking_date_time_end = models.DateTimeField(unique=True)
    def __str__(self):
        return str(self.table)