
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils import timezone

from survey.models import Survey, SurveyOption
from survey.forms import  SurveyChoiceForm


User = get_user_model()


def index_view(request):
    survey = create_inicial_data()
    context = {
        'survey_choice_form': SurveyChoiceForm(request.GET),
        'survey': survey,
    }
    return render(request, 'index.html', context)


def create_inicial_data():
    """
    Create initial data for the survey app.
    """

    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser(
            username='admin',
            password='admin',
        )

    survey = Survey.objects.filter(title='Test Survey').first()
    if not survey:
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

    return survey