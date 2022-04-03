import datetime
import inspect
import random
import sys
from pathlib import Path
from os import urandom
from base64 import b64encode

import sqlalchemy.exc
from pprintpp import pprint as pp
import names

sys.path.append(str(Path(__file__).parent.parent))

from app.factory import create_app
from app.models import db
from app.models.user import User

app = create_app('config.Development')


class UserGen:
    def __init__(self, email_sep: str = '', email_dn: str = 'test.com'):
        self._birthdate = None
        self._sex = None
        self._name = None
        self._fn = None
        self._ln = None
        self._un = None
        self._email = None
        self._password = None
        self._height = None
        self._weight = None
        self.email_sep = email_sep
        self.email_dn = email_dn

    def gen_sex(self):
        self._sex = random.choice(['male', 'female'])
        return self

    def gen_name(self):
        self._name = names.get_full_name(gender=self._sex)
        return self

    def gen_fn(self):
        self._fn = self._name.split()[0]
        return self

    def gen_ln(self):
        self._ln = self._name.split()[1]
        return self

    def gen_un(self, count: int = None):
        count_str: str = str(count) if count is not None else ''
        self._un = f"{self._fn[:1] + self._ln + count_str}".lower()
        return self

    def gen_pw(self):
        self._password = b64encode(urandom(15)).decode('utf-8')
        return self

    def gen_email(self, count: int = None):
        count_str: str = str(count) if count is not None else ''
        email_un = f'{self._fn + self.email_sep + self._ln + count_str}'.lower()
        email_domain = f'@{self.email_dn}'
        self._email = email_un + email_domain
        return self

    def gen_height(self):
        if self._sex == 'male':
            self._height = round(random.gauss(70.0, 3.0))
        if self._sex == 'female':
            self._height = round(random.gauss(64.5, 2.5))
        return self

    def gen_weight(self):
        if self._sex == 'male':
            self._weight = round(random.gauss(190.0, 59.0))
        elif self._sex == 'female':
            self._weight = round(random.gauss(156.5, 51.2))
        return self

    def gen_birthdate(self, min_age: int = None, max_age: int = None):
        start_date = (datetime.date.today()
                      - datetime.timedelta(days=max_age * 365))
        end_date = (datetime.date.today()
                    - datetime.timedelta(days=min_age * 365))
        diff = end_date - start_date
        self._birthdate = (
                start_date
                + datetime.timedelta(days=random.randrange(diff.days))
        )
        return self

    def populate(self):
        self.gen_sex()
        self.gen_name()
        self.gen_fn()
        self.gen_ln()
        self.gen_un()
        self.gen_height()
        self.gen_weight()
        self.gen_email()
        self.gen_pw()
        self.gen_birthdate(min_age=18, max_age=100)

        return self

    def generate(self) -> User:
        user = User(
            username=self._un,
            email=self._email,
            profile_completed=True,
            first_name=self._fn,
            last_name=self._ln,
            birthdate=self._birthdate,
            height=self._height,
            weight=self._weight,
        )
        user.set_password(self._password)
        return user

    def props(self):
        props = {}

        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                props[name] = value

        return props

    def __repr__(self):
        return f"<UserGen {self._un}>"


def add_user(user: UserGen, count: int = 0) -> None:
    user = user.generate()
    db.session.add(user)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        count = count + 1
        user._un = user.gen_un(count=count)
        user._email = user.gen_email(count=count)
        add_user(user, count)
    pp(user)


def create_users(num_users: int = 1) -> None:
    with app.app_context():
        for i in range(num_users):
            add_user(UserGen().populate())


if __name__ == '__main__':
    create_users(100)

# vim: ft=python ts=4 sw=4 sts=4 et
