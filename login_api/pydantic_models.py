from pydantic import BaseModel, validator
from email_validator import validate_email
from typing import Union
import validators
import re


class User(BaseModel):
    name: str
    surname: str
    username: str
    email: str
    password: str
    secure_auth: bool = False

    @validator("email")
    def is_valid_email(cls, email):
        validate_email(email, check_deliverability=True)

        return email

    @validator("password")
    def is_valid_password(cls, password):
        special_chars = re.compile('[@_!#$%^&*()<>?/\\\|}{~:]')  # TODO => test
        if len(password) < 8 \
                or not special_chars.search(password) \
                or re.search('[0-9]', password) is None \
                or re.search('[A-Z]', password) is None \
                or re.search('[a-z]', password) is None:
            raise ValueError(f"Password must be minimum 8 chars,"
                             f" must have both upper and lower case,"
                             f" must have at least 1 number and"
                             f" must contain special chars; "
                             f"'{password}' is not valid")

        return password


class Token(BaseModel):
    access_token: Union[str, dict]
    token_type: str


class OTP(BaseModel):
    password: str
    username: str


class Credentials(BaseModel):
    username: str
    password: str
