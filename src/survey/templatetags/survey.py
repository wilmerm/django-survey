from django import template

from survey.models import Survey

register = template.Library()


@register.inclusion_tag("survey/widgets/survey_detail.html", takes_context=True)
def survey_detail(context, survey):
    request = context['request']

    if isinstance(survey, str):
        survey = Survey.objects.get(pk=survey)

    context.update({
        'survey': survey,
        'survey_json': {
            'title': survey.title,
            'description': survey.description,
            'start_date': str(survey.start_date),
            'end_date': str(survey.end_date),
            'options': list(survey.options.filter(is_active=True).values('title', 'color', 'vote_count')),
        }
    })

    if request.user.is_authenticated:
        user_choices = request.user.survey_choices.all()
        context['user_choice'] = user_choices.filter(option__survey=survey).first()
        context['user_choices'] = user_choices

    return context