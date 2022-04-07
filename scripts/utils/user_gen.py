import sys
import random
import inspect
import datetime
from os import urandom
from pathlib import Path
from base64 import b64encode

import names

sys.path.append(str(Path(__file__).parent.parent))

from app.models.user import User


class UserGen:
    """Class to generate random User database models."""
    def __init__(self, email_sep: str = '', email_dn: str = 'test.com') -> None:
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
        """Randomly chooses a sex from female or male.

        Used to select between female and male names for the names module.

        :return: self
        """
        self._sex = random.choice(['male', 'female'])
        return self

    def gen_name(self):
        """Generates a random name for the user.

        Uses the python names module.

        :return: self
        """
        self._name = names.get_full_name(gender=self._sex)
        return self

    def gen_fn(self):
        """Splits first name from name.

        :return: self
        """
        self._fn = self._name.split()[0]
        return self

    def gen_ln(self):
        """Splits last name from name.

        :return: self
        """
        self._ln = self._name.split()[1]
        return self

    def gen_un(self, count: int = None):
        """Generate a username.

        :param count: optional parameter used to add a digit to the end of
                      username
        :return: self
        """
        count_str: str = str(count) if count is not None else ''
        self._un = f"{self._fn[:1] + self._ln + count_str}".lower()
        return self

    def gen_pw(self):
        """Randomly generates a password encoded in base64

        :return: self
        """
        self._password = b64encode(urandom(15)).decode('utf-8')
        return self

    def gen_email(self, count: int = None):
        """Generates an email address.

        :param count: optional parameter used to add a digit to the end of email
        :return: self
        """
        count_str: str = str(count) if count is not None else ''
        email_un = f'{self._fn + self.email_sep + self._ln + count_str}'.lower()
        email_domain = f'@{self.email_dn}'
        self._email = email_un + email_domain
        return self

    def gen_height(self):
        """Generates a random height based on sex.

        Gaussian distribution numbers taken from random survey of US citizens.

        :return: self
        """
        if self._sex == 'male':
            self._height = round(random.gauss(70.0, 3.0))
        if self._sex == 'female':
            self._height = round(random.gauss(64.5, 2.5))
        return self

    def gen_weight(self):
        """Generates a random weight based on sex.

        Gaussian distribution numbers taken from random survey of US citizens.

        :return: self
        """
        if self._sex == 'male':
            self._weight = round(random.gauss(190.0, 59.0))
        elif self._sex == 'female':
            self._weight = round(random.gauss(156.5, 51.2))
        return self

    def gen_birthdate(self, min_age: int = None, max_age: int = None):
        """Generates a random birthdate.

        Calculates the difference in days between the max age and min age and
        chooses a random number of days inbetween the two. The birthdate is then
        calculated from the random number of days.

        :param min_age: integer minimum age in years
        :param max_age: integer maximum age in years
        :return: self
        """
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
        """Calls all generator functions in the appropriate order.

        :return: self
        """
        self.gen_sex()
        self.gen_name()
        self.gen_fn()
        self.gen_ln()
        self.gen_un()
        self.gen_height()
        self.gen_weight()
        self.gen_email()
        self.gen_pw()
        # just randomly picked an age range, yolo
        self.gen_birthdate(min_age=18, max_age=100)

        return self

    def generate(self) -> User:
        """Generates a User database model populated with UserGen fields.

        :return: User database model
        """
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

    def props(self) -> dict:
        """Dictionary of all the fields in UserGen.

        Used from printing.

        :return: dict containing all fields in UserGen
        """
        props = {}

        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                props[name] = value

        return props

    def __repr__(self) -> str:
        return f"<UserGen {self._un}>"

# vim: ft=python ts=4 sw=4 sts=4 et
