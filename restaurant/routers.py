from tablebooking.views import TableView,ReservationView
from rest_framework import routers 

router = routers.DefaultRouter()
router.register("table", TableView)
router.register("booking", ReservationView)
