from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()


@nav.navigation()
def navbar() -> Navbar:
    return Navbar('Fitness App',
                  View('Home', 'index'),
                  View('Login', 'login'),
                  View('Logout', 'logout'),
                  View('Register', 'register'),
                  View('Meals', 'meals'),
                  View('Exercises', 'exercises'))

# vim: ft=python ts=4 sw=4 sts=4
