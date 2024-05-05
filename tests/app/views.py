
from django.shortcuts import render

from survey.forms import SurveyChoiceForm


def index_view(request):
    context = {
        'survey_choice_form': SurveyChoiceForm(request.GET),
    }
    return render(request, 'index.html', context)