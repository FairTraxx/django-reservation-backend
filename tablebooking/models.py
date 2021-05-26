
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
    people = models.IntegerField()
    booking_date_time_start = models.DateTimeField()
    booking_date_time_end = models.DateTimeField()
    SLOTS = (
        (1, _('12:00PM to 3:00PM')),
        (2, _('3:00PM to 6:00PM')),
        (3, _('6:00PM to 9:00PM')),
        (4, _('9:00PM to 11:59PM')),
    )
    time_slots = models.PositiveSmallIntegerField(
        default=1,
        choices=SLOTS,
    )
