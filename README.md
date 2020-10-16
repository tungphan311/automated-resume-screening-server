# Automated Resume Screening

:bulb: The official API for the automated resume screening (UIT Graduation Project)

## Installation

- Download and install [XAMPP](https://www.apachefriends.org/index.html), [Git](https://git-scm.com/) and [Python](https://www.python.org/).
- (For MacOS users only) Watch [this video](https://www.youtube.com/watch?v=yyjBFiXsOkI) to configure XAMPP on MacOS in order to work with phpmyadmin properly.
- After successfully installing XAMPP, click to start **Apache** and **MySQL** modules inside the **XAMPP Control Panel**.
- Visit `http://localhost/phpmyadmin` or `http://127.0.0.1/phpmyadmin`, create a new user and then create a new database with `utf8_unicode_ci` encoding.
- Clone this repository to your computer and move into it:

- Install required packages:

```
$ pip install -r requirements.txt
```

- Modify the `SQLALCHEMY_DATABASE_URI` value inside the `DevelopmentConfig` class inside the `app/main/config.py` file to match your MySQL username, password and database name.

```
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://<MYSQL_USERNAME>:<MYSQL_PASSWORD>@localhost/<MYSQL_DATABASE_NAME>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

- Run migration commands to update the database:

```
$ python manage.py db init
$ python manage.py db migrate -m Migration-Message
$ python manage.py db upgrade
```

- Run the API by typing this line:

```
$ python manage.py run
```

- Visit `http://localhost:5000` or `http://127.0.0.1:5000` to start interacting with the API via Swagger UI.

## Notes

- Always remember to create a new migration and update the database if a new model is created or an existing one is modified.
- Some routes require a user's token to get proceed. In that case, don't forget to set the `Authorization` value within the request's header to a user's token.
- If the `Authorization` key is already provided but still does not work, re-check to make sure that the user is also an administrator.
