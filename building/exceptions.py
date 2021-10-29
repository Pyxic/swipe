# exceptions.py
from rest_framework.exceptions import APIException


class AlreadyExist(APIException):
    status_code = 400
    default_detail = "User already has this announcement in favorites"
    default_code = "already has announcement"
