# exceptions.py
from rest_framework.exceptions import APIException


class AlreadyExist(APIException):
    status_code = 400
    default_detail = "User already has this announcement in favorites"
    default_code = "already has announcement"


class AdvantageAlreadyExist(AlreadyExist):
    default_detail = "complex already has this advantage"
    default_code = "already has advantage"
