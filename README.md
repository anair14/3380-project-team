# 3380 Project

## Members
* Ashwin Nair
* Austin McBurney
* Christian Pentavin
* Brandon Domangue 
* Jonathan Lagarrigue
* Jacob Carter
* David Robins

## Installing
We're using version 3.9.10 of Python due to issues with SQLAlchemy and Python 3.10.
Make sure to install 3.9.10 before proceeding.

Execute the following commands while in the project directory:
```shell
python -m venv venv

# for windows, use powershell
venv\Scripts\activate.ps1

# UNIX or macOS
source venv/bin/activate

pip install -r requirements.txt -r requirements-dev.txt
```

## Database Setup
The database must be configured before running the application.

If you have GNU make installed on your system, you can run:

```shell
make db-re
```

If you do not have make installed, run:

```shell
flask db init
flask db migrate
flask db upgrade
```

This will create a new database from scratch without any users registered.
You are then able to register a new user and sign in.

## Running
Once you have everything installed, you can run the app by running the following
commands in the project directory:

```shell
flask run
```

## Configuration
You can edit configuration values in config.py, but the defaults set are sane.
