from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import SurveyChoiceForm
from .models import Survey, SurveyChoice, SurveyOption


class SurveyDetailView(DetailView):
    queryset = Survey.objects.filter(is_active=True)


@login_required
@require_POST
def vote_view(request):
    survey_option = get_object_or_404(SurveyOption, pk=request.POST.get('survey_option_id'))
    success_url = request.POST.get('success_url')
    form = SurveyChoiceForm({
        'option': survey_option,
        'user': request.user,
    })
    if form.is_valid():
        survey_choice = form.save()
    return HttpResponseRedirect(success_url)