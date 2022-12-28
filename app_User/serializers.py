from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from .models import User, PHONE_NUMBER_REGEX_VALIDATOR, Address
from .utils import Redis, Manage_SMS_Portal


class UserRegisterSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'password_did_not_match': {
            'status': False,
            'message': _('رمز عبور و تکرار آن یکی نیستند'),
            'field': 'password'
        }
    }

    mobile_number = serializers.CharField(
        required=True,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR, UniqueValidator(queryset=User.objects.all(), message='این شماره تلفن از قبل موجود میباشد')],
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
    )
    re_password = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'mobile_number',
            'password',
            're_password'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise exceptions.ParseError(
                self.error_messages['password_did_not_match'], 'password_did_not_match'
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            mobile_number=validated_data['mobile_number'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserVerifyRegisterSerializer(serializers.Serializer):
    default_error_messages = {
        'user_not_found': {
            'status': False,
            'message': _('کاربر مورد نظر پیدا نشد')
        },
        'otp_code_expired': {
            "status": False,
            "message": _("زمان اعتبار کد ارسال شده به پایان رسیده است")
        },
        'invalid_otp_code': {
            "status": False,
            "message": _("کد وارد شده اشتباه است، لطفا دوباره سعی کنید")
        },
    }
    mobile_number = serializers.CharField(
        required=True,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR, ],
    )

    otp_code = serializers.IntegerField(
        required=True,
    )

    def validate(self, attrs):
        user_obj = User.objects.filter(mobile_number=attrs['mobile_number']).first()
        if user_obj is None:
            raise exceptions.ParseError(
                self.error_messages['user_not_found'], 'user_not_found'
            )
        redis_management = Redis(user_obj.mobile_number, 'sms_verification')
        result_check_validate = redis_management.validate(attrs['otp_code'])
        if result_check_validate is None:
            raise exceptions.ParseError(
                self.error_messages['otp_code_expired'], 'otp_code_expired'
            )
        else:
            if result_check_validate is False:
                raise exceptions.ParseError(
                    self.error_messages['invalid_otp_code'], 'invalid_otp_code'
                )
            else:
                redis_management.delete()
                user_obj.activate()
                return True


class UserReSendRegisterOTPCodeSerializer(serializers.Serializer):
    default_error_messages = {
        'user_not_found': {
            'status': False,
            'message': _('کاربر مورد نظر پیدا نشد')
        },
    }
    mobile_number = serializers.CharField(
        required=True,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR, ],
    )

    def validate(self, attrs):
        user_obj = User.objects.filter(mobile_number=attrs['mobile_number']).first()
        if user_obj is None or user_obj.is_active:
            raise exceptions.ParseError(
                self.error_messages['user_not_found'], 'user_not_found'
            )
        redis_management = Redis(user_obj.mobile_number, 'sms_verification')
        if redis_management.exists():
            raise exceptions.ParseError({
                'status': False,
                'message': _('کد فعالسازی از قبل ارسال شده است'),
                'time': redis_management.get_expire()
            })
        else:
            manage_sms_obj = Manage_SMS_Portal(user_obj.mobile_number)
            manage_sms_obj.send_otp_code()
            return True


class UserLoginSerializer(serializers.Serializer):
    default_error_messages = {
        'user_not_registered_or_invalid_password': {
            'status': False,
            'message': _('شماره موبایل یا رمزعبور اشتباه است')
        },
        'user_not_activated': {
            'status': False,
            'message': _('حساب شما فعال نمیباشد، لطفا نسبت به فعالسازی حساب کاربری خود اقدام کنید'),
            'accountActivationError': True
        },
    }
    mobile_number = serializers.CharField(
        required=True,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR, ],
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate(self, attrs):
        user_obj = User.objects.filter(mobile_number=attrs['mobile_number']).first()
        if user_obj is None or user_obj.check_password(attrs['password']) is False:
            raise exceptions.ParseError(
                self.error_messages['user_not_registered_or_invalid_password'], 'user_not_registered_or_invalid_password'
            )
        else:
            if user_obj.is_active is False:
                manage_sms_obj = Manage_SMS_Portal(user_obj.mobile_number)
                manage_sms_obj.send_otp_code()
                raise exceptions.ParseError(
                    self.error_messages['user_not_activated'], 'user_not_activated'
                )
            else:
                user_obj.set_last_login()
                user_token = Token.objects.get(user=user_obj)
                return {
                    "id": user_obj.id,
                    "first_name": user_obj.first_name,
                    "last_name": user_obj.last_name,
                    "mobile_number": user_obj.mobile_number,
                    "auth_token": user_token.key
                }


class CompleteUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name'
        ]
        extra_kwargs = {
            'first_name': {
                'required': True
            },
            'last_name': {
                'required': True
            },
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
    )
    new_re_password = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "old_password",
            "new_password",
            "new_re_password",
        ]

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("رمز عبور قبلی صحیح نمیباشد")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_re_password']:
            raise exceptions.ParseError({
                "new_password": "رمز عبور و تکرار رمز عبور یکی نیستند",
                "new_re_password": "رمز عبور و تکرار رمز عبور یکی نیستند",
            })
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "address_description",
            "post_code",
            "receiver",
            "receiver_mobile_number",
        ]
        read_only_fields = [
            "id",
        ]

    def validate(self, attrs):
        attrs.update({'user': self.context.get('request').user})
        return attrs
