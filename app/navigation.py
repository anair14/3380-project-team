from flask_nav import Nav
from flask_nav.elements import Navbar, View, Text, Separator

nav = Nav()


@nav.navigation()
def auth_nav() -> Navbar:
    return Navbar('Fitness App',
                  View('Home', 'index'),
                  View('Exercises', 'exercises'),
                  View('Meals', 'meals'),
                  View('Profile', 'profile'),
                  View('Account', 'account'),
                  View('Logout', 'logout'))


@nav.navigation()
def not_auth_nav() -> Navbar:
    return Navbar('Fitness App',
                  View('Login', 'login'),
                  View('Register', 'register'))


class AuthenticatedUser(Text):
    def __init__(self, text):
        super().__init__(text)

    @property
    def text(self):
        return

# vim: ft=python ts=4 sw=4 sts=4
