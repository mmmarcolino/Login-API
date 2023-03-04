import datetime
from login_api.pydantic_models import Token, User
from pypika import Table, MySQLQuery


def adapt_email_and_username_to_user_query(email: str, username: str) -> str:
    user_table = Table('users')
    query = MySQLQuery.from_(user_table).select('*')\
        .where((user_table.email == email) | (user_table.username == username))

    return f'{query.get_sql()};'


def adapt_email_to_user_query(email: str) -> str:
    user_table = Table('users')
    query = MySQLQuery.from_(user_table).select('*') \
        .where(user_table.email == email)

    return f'{query.get_sql()};'


def adapt_username_to_user_query(username: str) -> str:
    user_table = Table('users')
    query = MySQLQuery.from_(user_table).select('*') \
        .where(user_table.username == username)

    return f'{query.get_sql()};'


def adapt_user_creation_to_query(user: dict):
    user_table = Table('users')
    query = MySQLQuery.into(user_table).columns(*user.keys()).insert(*user.values())

    return f'{query.get_sql()};'


def adapt_db_user_to_model(name: str, surname: str, username: str, email: str, password: str, secure_auth: bool):
    return User(
        name=name,
        surname=surname,
        username=username,
        email=email,
        password=password,
        secure_auth=secure_auth
    )


def adapt_user_to_token_data(username: str):
    return {
        'sub': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }


def adapt_token_to_model(token: str, token_type: str):
    return Token(
        access_token=token,
        token_type=token_type
    )
