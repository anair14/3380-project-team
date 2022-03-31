import random
import sys
from pathlib import Path
from os import urandom
from base64 import b64encode
from typing import List
from pprintpp import pprint as pp
import names

sys.path.append(str(Path(__file__).parent.parent))

from app.factory import create_app
from app.models import db
from app.models.user import User

app = create_app('config.Development')


class UserGen:
    def __init__(self, first_name: str = None, last_name: str = None,
                 username: str = None,
                 email: str = None,
                 password: str = None, email_sep: str = '',
                 email_dn: str = 'test.com'):
        self.fn = first_name
        self.ln = last_name
        self.un = username
        self.email = email
        self.password = password
        self.email_sep = email_sep
        self.email_dn = email_dn

    def gen_un(self):
        return f"{fn[:1] + ln}".lower()

    def gen_pw(self):
        return b64encode(urandom(15)).decode('utf-8')

    def gen_email(self):
        email_un = f'{self.fn + self.email_sep + self.ln}'.lower()
        email_domain = f'@{self.email_dn}'
        return email_un + email_domain

    def gen_fn_ln(self):
        [fn, ln] = names.get_full_name().split(' ')
        return [fn, ln]

    def populate(self):
        self.fn = self.fn or fn
        self.ln = self.ln or ln
        self.un = self.un or self.gen_un()
        self.email = self.email or self.gen_email()
        self.password = self.password or self.gen_pw()
        return self

    def generate(self) -> User:
        return User(
            username=self.un,
            email=self.email,
            profile_completed=True,
            first_name=self.fn,
            last_name=self.ln,
            height=random.randint(40, ),

        ).password_hash(self.password)

    def __repr__(self):
        return f"<UserGen {self.un}>"


def create_user_list(num_users: int = 1) -> list[UserGen]:
    return [UserGen().populate() for x in range(num_users)]


def create_users(num_users: int = 1) -> None:
    pass


if __name__ == '__main__':
    users = create_user_list(num_users=10)
    pp(users)

# vim: ft=python ts=4 sw=4 sts=4 et
