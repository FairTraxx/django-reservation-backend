import json 
from users.models import NewUser
from django.urls import reverse
from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.serializers import CustomUserSerializer
#and import any model to test


class ProfileViewTestCase(APITestCase):
    def test_setUp(self):
        self.user = NewUser.objects.create_user(employee_id =1200, user_name = 'averyuniqueusername', password = 'AveryStrongpassword')
        self.token = Token.objects.create(user = self.user)
        self.api_authentication()

    def test_api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION = "Token" + self.token)