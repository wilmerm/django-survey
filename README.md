# django-survey
The "django-survey" project is an application for Django that makes it easy to create and manage surveys on websites. This application provides functionalities to create surveys, define questions and response options, manage active and inactive surveys, collect user responses, and generate statistical reports on survey results. With this tool, developers can easily integrate surveys into their Django websites to collect user data and feedback.

## Instalation

```sh
pip install django-surveyplus
```

## Use

### Add to installed applications

```py
# settings.py

INSTALLED_APPS = [
    # ...
    'survey',
    # ...
]
```

### Add the URLs

```py
urlpatterns = [
    # ...
    path('survey/', include('survey.urls')),
    # ...
]
```

### Run the migrations

```sh
python manage.py migrate
```

## Licence

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Proyect Status

This project is in Production/Stable ✔

## Contribution 💗

If you find value in this project and would like to show your support, please consider making a donation via PayPal:

[Donate on PayPal](https://paypal.me/martinezwilmer?country.x=DO&locale.x=es_XC)

Your generosity helps us to continue improving and maintaining this project. We appreciate every contribution, however small. Thanks for being part of our community!
