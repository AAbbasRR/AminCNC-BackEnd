from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager

from jalali_date import datetime2jalali


class UserManager(BaseUserManager):
    """
    Inherit from BaseUserManager for create custom manager methods
    """
    use_in_migrations = True

    def _create_user(self, mobile_number, password, **extra_fields):
        """
        :param mobile_number: user mobile number want to create
        :param password: user password want to create
        :param extra_fields: kwargs User Model
        :return: create new user with params and return user object
        """
        if not mobile_number:
            raise ValueError('The given mobile_number must be set')
        user = self.model(mobile_number=mobile_number, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile_number=None, password=None, **extra_fields):
        """
        :param mobile_number: user mobile number want to create
        :param password: user password want to create
        :param extra_fields: kwargs User Model
        :return: Create and save a regular User with the given email or mobile_number and password.
        Note: The username of the user is mobile number and email, his storage with mobile or email is optional
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile_number, password, **extra_fields)

    def create_superuser(self, mobile_number, password, **extra_fields):
        """
        :param password: user password want to create
        :param extra_fields: kwargs User Model
        :return: Create and save a SuperUser with the given email and password.
        Note: this method writed for coommand `createsuperuser`, after create superuser set user type admin
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self._create_user(mobile_number, password, **extra_fields)
        return user


PHONE_NUMBER_REGEX_VALIDATOR = RegexValidator(r'^{?(0?9[0-9]{9,9}}?)$', 'شماره موبایل نامعتبر')


class User(AbstractUser):
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = f"{verbose_name}ان"

    username = None
    email = None
    mobile_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR],
        verbose_name='شماره موبایل'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='وضعیت فعال بودن حساب'
    )
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.mobile_number} - {self.first_name}"

    def get_jalali_date_joined(self):
        return datetime2jalali(self.date_joined).strftime('%Y/%m/%d _ %H:%M:%S')

    def get_jalali_last_login(self):
        return datetime2jalali(self.last_login).strftime('%Y/%m/%d _ %H:%M:%S')

    def activate(self) -> object:
        """
        :return: active user account after email account validate
        """
        self.is_active = True
        self.save()
        return self

    def set_last_login(self) -> object:
        """
        :return: When the user logs in, we record her login time as the last login time
        """
        self.last_login = timezone.now()
        self.save()
        return self


class Address(models.Model):
    class Meta:
        verbose_name = "آدرس های کاربر"
        verbose_name_plural = f"{verbose_name}ان"

    user = models.ForeignKey(
        User,
        related_name='address_user',
        on_delete=models.CASCADE,
        verbose_name='کاربر',
    )
    address_description = models.TextField(
        null=False,
        blank=False,
        verbose_name='توضیحات آدرس'
    )
    post_code = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        verbose_name='کد پستی'
    )
    receiver = models.CharField(
        max_length=75,
        null=False,
        blank=False,
        verbose_name='نام و نام خانوادگی گیرنده'
    )
    receiver_mobile_number = models.CharField(
        max_length=11,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR],
        verbose_name='شماره موبایل گیرنده'
    )

    def __str__(self) -> str:
        return f"{self.user.mobile_number} - {self.receiver}"
