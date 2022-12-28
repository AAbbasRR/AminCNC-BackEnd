from amincnc import settings

import random
import redis
import requests


class Redis:
    """
    manage user keys on redis
    """
    cache = redis.StrictRedis(
        decode_responses=True,
        host=settings.Redis_host,
        port=settings.Redis_port,
        db=settings.Redis_db
    )  # config redis system cache

    def __init__(self, mobile, key):  # For the key to be unique, we use the user's email to access the key and a string for the key to be unique and clear.
        self.key = mobile + key

    def set_value(self, value):  # Set a value on the key in Radis
        self.cache.set(self.key, value)

    def get_value(self):  # Returns the internal value of the key
        if self.cache.exists(self.key):
            return self.cache.get(self.key)
        else:
            return None

    def set_expire(self, time=300):  # Set a time for the key to expire (time is in seconds)
        self.cache.expire(self.key, time)

    def get_expire(self):  # Returns the number of seconds remaining before the key expires
        return self.cache.ttl(self.key)

    def validate(self, user_value):  # Takes an input value and checks to see if it is the same as the value inside the key
        user_value = str(user_value)
        if self.cache.exists(self.key):
            redis_value = self.cache.get(self.key)
            if redis_value == user_value:
                return True
            else:
                return False
        else:
            return None

    def exists(self):  # Checks if the key is there or not
        return self.cache.exists(self.key) == 1

    def delete(self):  # Remove the key from Radis
        return self.cache.delete(self.key)


def create_otp_code(length=5):  # create a random digit number
    return str(random.randint((10 ** (length - 1)), (10 ** length - 1)))


class Manage_SMS_Portal:
    def __init__(self, user_mobile):
        self.user_mobile = user_mobile

    def send_otp_code(self):
        manage_redis = Redis(self.user_mobile, 'sms_verification')
        otp_code = create_otp_code()
        manage_redis.set_value(otp_code)
        manage_redis.set_expire(settings.SMS_VERIFICATION_TIME_EXPIRE)
        request_response = requests.post(
            "https://raygansms.com/SendMessageWithCode.ashx",
            data={
                "UserName": settings.SMS_PORTAL['username'],
                "Password": settings.SMS_PORTAL['pass'],
                "Mobile": self.user_mobile,
                "Message": f"به امینcnc خوش آمدید، کد فعالسازی شما {otp_code} میباشد."
            }
        )
        if request_response.status_code == 200:
            return True
        else:
            print(request_response)
            return False

    def send_auto_otp_code(self):
        request_response = requests.post(
            "https://raygansms.com/AutoSendCode.ashx",
            data={
                "UserName": settings.SMS_PORTAL['username'],
                "Password": settings.SMS_PORTAL['pass'],
                "Mobile": self.user_mobile,
                "Footer": "خرید محصولات چوبی از amincnc.ir"
            }
        )
        if request_response.status_code == 200:
            return True
        else:
            print(request_response)
            return False

    def check_auto_otp_code(self, otp_code):
        request_response = requests.post(
            "https://raygansms.com/CheckSendCode.ashx",
            data={
                "UserName": settings.SMS_PORTAL['username'],
                "Password": settings.SMS_PORTAL['pass'],
                "Mobile": self.user_mobile,
                "Code": str(otp_code)
            }
        )
        if request_response.status_code == 200:
            return True
        else:
            print(request_response)
            return False
