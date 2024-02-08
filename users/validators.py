import os

import requests
from rest_framework.serializers import ValidationError


class EmailValidators:

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        email = dict(value).get(self.fields[0])
        api_key = os.getenv('API_KEY')
        try:
            response = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}")
            result = response.json()['data']['result']
        except Exception:
            raise ValidationError("Ошибка проверки адреса электронной почты")
        if result != 'deliverable':
            raise ValidationError("адрес электронной почты недействителен")
