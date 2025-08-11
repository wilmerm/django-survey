from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import SurveyChoiceForm
from .models import Survey, SurveyChoice, SurveyOption


class SurveyDetailView(DetailView):
    queryset = Survey.objects.filter(is_active=True)


@require_POST
def vote_view(request):
    survey_option = get_object_or_404(SurveyOption, pk=request.POST.get('survey_option_id'))
    success_url = request.POST.get('success_url')
    survey = survey_option.survey
    
    # Check if survey requires authentication
    if survey.requires_authentication and not request.user.is_authenticated:
        messages.error(request, _("You must be logged in to vote on this survey."))
        return HttpResponseRedirect(success_url)
    
    # Ensure session exists for anonymous users
    if not request.user.is_authenticated:
        if not request.session.session_key:
            request.session.save()
    
    # Prepare form data
    form_data = {'option': survey_option}
    
    if request.user.is_authenticated:
        form_data['user'] = request.user
    else:
        form_data['session_key'] = request.session.session_key
    
    form = SurveyChoiceForm(form_data)
    
    try:
        if form.is_valid():
            survey_choice = form.save()
            messages.success(request, _("Your vote has been recorded successfully."))
        else:
            # Extract form errors and display them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    except ValidationError as e:
        messages.error(request, str(e))
    
    return HttpResponseRedirect(success_url)