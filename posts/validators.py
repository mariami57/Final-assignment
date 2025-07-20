import re
from typing import Optional

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class OtherDestinationFormatValidator:
    def __init__(self, message:Optional[str]=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value or 'Please enter a valid destination format'

    def __call__(self, value):
        if not re.fullmatch(r'[A-Za-z]+,[A-Za-z]+', value):
            raise ValidationError(self.message)