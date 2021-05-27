## Django RESTaurant API

This my take for the restaurant task that was provided, the API contains User authentication with the required roles, and endpoints to perform all the required table and booking functionality.

However, unfortuantly due to the insufficent time frame resulting from my back 2 back midterm exams, 80% of the development was done in a single day with tons of coffee, So I did my best to cover all the core functionality and edge cases but unfortuantly didn't have time to write extensive unit tests, So I will do my best to throughly explain everything in this README.

You can find the postman documentation here: https://documenter.getpostman.com/view/11720989/TzXxjyBD

### The reservation algorithm 

For the reservation algorithm it goes something like this (well commented in the code):

- get table, people, start/end dates from user

- query the tables and it's reservation to see if `people > tablesize` if so it throws an error that the number is insufficent and includes the table size that we can't exceed.

- We then check if the reservation is within working hours (12:00PM-11:59PM) and also its usefull to check at this point if there are any reservations at all so we can skip any unnecessary looping and book a slot right away.

- If we find a reservation on that table, we check if our reservation overlaps with it like so: 

```
_                        |---- DateRange A ------|
|---Date Range B -----| 
```
 This translates to `(StartDateA <= EndDateB) and (EndDateA >= StartDateB)` if this condition is satisfied then the dates overlap and we can't book that time slot, an expection is thrown. If not then we book the time slot.

 ### Get available time slots algorithm

 Now here is where things get a bit messy :D

 - Given only the number of people, we first check/catch if that number is within our range of maximum seats (1-12 seats)

 - We then query the tables with `people <= Table Seats` then we query all the reservations on those tables

 - We then iterate over all the reservations on those tables comparing the current date/time with the reserved date/time

 - if `currenttime < booking_start` we calculate a time slot starting from now up until the table starts to get reserved, then calculate another timeslot after the reservation ends up until a next reservation comes or we reach the end of working hours.

 - if `currenttime > booking_start` we calculate a time slot starting from `booking_end` all the way till either the next reservation or the end of the working hours.

 - We shoot this data to the poor employee working 12 hours a day (requiring authentication ofc)

### Instructions

- clone the git repository ` git clone https://github.com/FairTraxx/django-reservation-backend.git`

- `cd` into the cloned folder

- set up a virtual environment `python -m venv env`

- start it using `env\Scripts\activate`

- run `pip install -r requirements.txt` to install required packages

- start the server with `python manage.py runserver`

The database is connected to a postgres server running online, but a sqlite db is also included for quick access with some dummy data.

