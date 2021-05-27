from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import action
from django.http import JsonResponse, HttpResponse
from django.core import serializers as ser
from rest_framework.response import Response
from datetime import datetime
import json
from . import models
from . import serializers


class TableView(viewsets.ModelViewSet):
    queryset = models.Table.objects.all()
    serializer_class = serializers.TableSerializer
# Create your views here.
# list() retreive() create() destroy()


class ReservationView(viewsets.GenericViewSet):
    queryset = models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer

    @action(detail=False, methods=["get"], url_path="getreservations")
    def GetReservations(self, request):
        reservations = self.get_queryset().all()
        serializer = self.get_serializer_class()(reservations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add")
    def BookSlot(self, request):
        # query all reservations on the requested table
        booking_list = models.Booking.objects.filter(
            table=request.data['table'])
        # query the table so we can check it's size
        table_info = models.Table.objects.get(
            table_number=request.data['table'])
        if request.data['people'] > table_info.size:
            return JsonResponse(
                {"error": "Requested table doesn't have enough seats"}, status=status.HTTP_400_BAD_REQUEST
            )
        # convert str from request to datetime format so we can compare dates
        requested_start_date = datetime.strptime(
            request.data['booking_date_time_start'], '%Y-%m-%dT%H:%M:%S%z')
        requested_end_date = datetime.strptime(
            request.data['booking_date_time_end'], '%Y-%m-%dT%H:%M:%S%z')
        # Check if the requested times are within restaurant's working hours (using the same date provided)
        if requested_start_date < requested_start_date.replace(hour=12, minute=0, second=0, microsecond=0) or requested_end_date > requested_end_date.replace(hour=23, minute=59, second=0, microsecond=0):
            return JsonResponse(
                {"error": "Reservation time is outside working hours (12:00PM to 11:59PM)"}, status=status.HTTP_400_BAD_REQUEST
            )
        # data to be used in the reservations
        data = {
            "table": request.data["table"],
            "people": request.data["people"],
            "booking_date_time_start": requested_start_date,  # formatted date
            "booking_date_time_end": requested_end_date  # formatted date
        }
        # if there are no bookings at all, then book any slot within working hours
        if len(booking_list) == 0:
            serializer = serializers.BookingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Table reserved": serializer.data}, status=status.HTTP_201_CREATED)
        # Query all the reservations on the requested table and compare them with provided date
        for booking in booking_list:
            # check if the timeslot is available (this part is explained in the README)
            if booking.booking_date_time_start <= requested_end_date or requested_start_date <= booking.booking_date_time_end:
                return JsonResponse(
                    {"error": "Time Slot is already booked, check available timeslots first"}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # if our booking doesn't overlapp with existing booking then we reserve the table
                serializer = serializers.BookingSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Table reserved": serializer.data}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
