# django-survey

The **django-survey** project is an application for Django that makes it easy to create and manage surveys on websites. This application provides functionalities to create surveys, define questions and response options, manage active and inactive surveys, collect user responses, and generate statistical reports on survey results. With this tool, developers can easily integrate surveys into their Django websites to collect user data and feedback.

![image](https://github.com/wilmerm/django-survey/assets/44853160/abbfeede-8fd2-4cd4-bab8-d920c5974a09)

## Installation

```sh
pip install django-surveyplus
```

---

## Usage

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

### Creating a Survey

```py
from survey.models import Survey, SurveyOption

survey = Survey.objects.create(
    title='Test Survey',
    description='Survey Description',
)

for i in range(1, 5):
    SurveyOption.objects.create(
        survey=survey,
        title=f'Option {i}',
        description=f'Option {i} Description',
    )
```

### Displaying the Survey

```html
{% load survey %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Survey</title>
</head>
<body>
    <!-- Assuming you have a survey object -->
    {% survey_detail survey %}
</body>
</html>
```

---

## Developer Instructions

### Setting Up the Development Environment

1. **Clone the repository:**

    ```sh
    git clone https://github.com/wilmerm/django-survey.git
    cd django-survey
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

4. **Build and install the survey application:**

    ```sh
    python -m build
    pip uninstall django-surveyplus
    pip install dist/*tar.gz
    ```

5. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

### Running Tests

To run the tests, use the following command:

```sh
python manage.py test
```

### Building and Publishing the Library

To compile and upload the library to PyPI, follow these steps:

1. Ensure you have the necessary dependencies:

    ```sh
    pip install build twine
    ```

2. Build the package:

    ```sh
    python -m build
    ```

3. (Optional) Verify the package:

    ```sh
    twine check dist/*
    ```

4. Upload the package to PyPI:

    ```sh
    python -m twine upload dist/*
    ```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Project Status

This project is in Production/Stable ✔

---

## Contribution 💗

If you find value in this project and would like to show your support, please consider making a donation via PayPal:

[Donate on PayPal](https://paypal.me/martinezwilmer?country.x=DO&locale.x=es_XC)

Your generosity helps us to continue improving and maintaining this project. We appreciate every contribution, however small. Thanks for being part of our community!
