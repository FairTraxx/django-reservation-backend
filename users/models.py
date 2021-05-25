
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinLengthValidator, int_list_validator


class CustomAccountManager(BaseUserManager):
    # Create an admin account
    def create_superuser(self, user_name, employee_id, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(user_name, employee_id, password, **other_fields)
    # Create an employee account

    def create_user(self, user_name, employee_id, password, **other_fields):
        # if other_fields.is_superuser == False:
        #     raise ValueError(
        #         _('Unauthorized User creation, must be Admin to perform this operation'))

        if not employee_id:
            raise ValueError(_('You must provide an employee id'))
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_admin', True)
        #employee_id = self.normalize_employee_id(employee_id)
        #user_name = self.normalize_username(user_name)
        user = self.model(user_name=user_name,
                          employee_id=employee_id, role='Employee', **other_fields)
        user.set_password(password)
        user.save()
        return user
# Each user will have a name, an employee number, role, and a password


class NewUser(AbstractBaseUser, PermissionsMixin):

    employee_id = models.CharField(
        _('employee number'),
        max_length=4,
        validators=[int_list_validator(sep=''), MinLengthValidator(4), ],
        unique=True
    )
    user_name = models.CharField(max_length=150, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    ADMIN = 'Admin'
    EMPLOYEE = 'Employee'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (EMPLOYEE, 'Employee'),
    ]
    role = models.CharField(
        max_length=150,
        choices=ROLE_CHOICES,
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name
