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

## Running
Once you have everything installed, you can run the app by running the following
commands in the project directory:

```shell
flask run
```

## Configuration
You can edit configuration values in config.py, but the defaults set are sane.
