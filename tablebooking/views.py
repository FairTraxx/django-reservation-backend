from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from datetime import datetime
import json
from . import models
from . import serializers
from .models import Booking
import pytz

utc = pytz.UTC


class TableView(viewsets.ModelViewSet):
    queryset = models.Table.objects.all()
    serializer_class = serializers.TableSerializer
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination
# Create your views here.
# list() retreive() create() destroy()


class ReservationView(viewsets.ModelViewSet):
    queryset = models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer
    pagination_class = PageNumberPagination

    @action(detail=False, methods=["get"], url_path="checkavailable")
    @permission_classes([IsAuthenticated])
    def CheckTimeSlots(self, request):
        # catch if people pass 12 person
        if request.data['people'] > 12:
            return JsonResponse(
                {"error": "Invalid number of people,Tables can only have 12 seats or less"}, status=status.HTTP_400_BAD_REQUEST
            )
        # Query table list with size <= seat number
        table_list = models.Table.objects.filter(
            size__lte=request.data['people'])
        # User result from query above to query all rervations to that table
        booking_list = Booking.objects.filter(
            table__in=table_list.values_list('table_number', flat=True))
        # Empty array to store our time slots in
        json_res = []
        # Loop through reservations
        for booking in booking_list:
            # capture table number for each reservation
            table_no = str(booking.table)
            # get current time to calculate time slots
            now = datetime.now().replace(microsecond=0, tzinfo=utc)
            # get start and end datetime for reservation
            start = booking.booking_date_time_start
            end = booking.booking_date_time_end
            # Set the closing hour
            closing_time = datetime.now().replace(
                hour=23, minute=59, second=0, microsecond=0, tzinfo=utc)
            # set the slot from current time to start of reservation (if time.now<booked_start)
            # and also save the empty slot after that time
            if now < start:
                slot_1 = [now, start]
                slot_2 = [end, closing_time]
                json_obj = dict(
                    table=table_no,
                    slots=[slot_1] + [slot_2]
                )
                json_res.append(json_obj)
            else:
                slot_2 = [end, closing_time]
                json_obj = dict(
                    table=table_no,
                    slots=[slot_2]
                )
                json_res.append(json_obj)
        return Response(json_res)

    @action(detail=False, methods=["get"], url_path="getreservations")
    @permission_classes([IsAuthenticated])
    def GetReservations(self, request):
        # get all reservations
        reservations = self.get_queryset().all()
        serializer = self.get_serializer_class()(reservations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path="delete")
    @permission_classes([IsAuthenticated])
    def delete(self, request):
        # delete a reservation
        # count = Tutorial.objects.all().delete()
        reservations = models.Booking.objects.filter(
            pk=request.data['id']).delete()
        return JsonResponse(
                {"deleted reservation number": request.data['id']}, status=status.HTTP_204_NO_CONTENT
            )
    # Book a time slot

    @action(detail=False, methods=["post"], url_path="add")
    @permission_classes([IsAuthenticated])
    def BookSlot(self, request):
        # query all reservations on the requested table
        booking_list = models.Booking.objects.filter(
            table=request.data['table'])
        # query the table so we can check it's size
        table_info = models.Table.objects.get(
            table_number=request.data['table'])
        if request.data['people'] > table_info.size:
            return JsonResponse(
                {"error": "Requested table number of seats is insufficent",
                 "Table Number": request.data['table'],
                 "Number of seats": table_info.size}, status=status.HTTP_400_BAD_REQUEST
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
            if booking.booking_date_time_start <= requested_end_date and requested_start_date <= booking.booking_date_time_end:
                return JsonResponse(
                    {"error": "Time Slot is already booked, check available timeslots first"}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # else our booking doesn't overlap with existing booking then we reserve the table
                serializer = serializers.BookingSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Table reserved": serializer.data}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
