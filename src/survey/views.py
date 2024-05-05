import json
from typing import Any
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse

from .forms import SurveyChoiceForm
from .models import Survey, SurveyChoice, SurveyOption


class SurveyDetailView(DetailView):
    queryset = Survey.objects.filter(is_active=True)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        survey = self.get_object()
        context['survey_json'] = {
            'title': survey.title,
            'description': survey.description,
            'start_date': survey.start_date,
            'end_date': survey.end_date,
            'options': serialize('dict', survey.options.filter(is_active=True)),
        }
        if self.request.user.is_authenticated:
            user_choices = self.request.user.survey_choices.all()
            context['user_choice'] = user_choices.filter(option__survey=survey).first()
            context['user_choices'] = user_choices
        return context


@login_required
@require_POST
def vote_view(request):
    survey_option = get_object_or_404(SurveyOption, pk=request.POST['survey_option_id'])
    form = SurveyChoiceForm({
        'option': survey_option,
        'user': request.user,
    })
    if form.is_valid():
        survey_choice = form.save()
    return HttpResponseRedirect(survey_option.survey.get_absolute_url())