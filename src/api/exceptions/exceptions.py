import typing
import uuid

import fastapi


class ICustomException(Exception):
    status_code: int
    message: str


class EntityNotFoundException(ICustomException):
    def __init__(self, entity_name: str, entity_id: uuid.UUID = None):
        self.status_code = fastapi.status.HTTP_404_NOT_FOUND
        if entity_id is None:
            self.message = f'{entity_name.capitalize()} not found'
        else:
            self.message = f'{entity_name.capitalize()} with id: {entity_id}, doesnt exist'


class EntityAlreadyExistException(ICustomException):
    def __init__(self, entity_name: str):
        self.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        self.message = f'{entity_name.capitalize()} with specified fields already exist'


class RateYourselfPostException(ICustomException):
    def __init__(self):
        self.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        self.message = 'You didnt rate yourself posts'


class WrongPasswordException(ICustomException):
    def __init__(self):
        self.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        self.message = 'Wrong password'


CUSTOM_EXCEPTIONS: list[typing.Type[ICustomException]] = [
    EntityNotFoundException,
    EntityAlreadyExistException,
    RateYourselfPostException,
    WrongPasswordException,
]
