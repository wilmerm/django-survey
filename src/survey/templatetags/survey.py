from django import template

from survey.models import Survey

register = template.Library()


@register.inclusion_tag("survey/widgets/survey_detail.html", takes_context=True)
def survey_detail(
    context,
    survey: Survey | str,
    show_title: bool = True,
    show_description: bool = True,
    show_image: bool = True,
    success_url: str = None,
    row_class: str = 'row justify-content-center mb-5',
):
    """
    Render a survey detail widget.

    Args:
        context: The template context.
        survey: The survey object or its ID.
        show_title: Whether to show the survey title.
        show_description: Whether to show the survey description.
        show_image: Whether to show the survey image.
        success_url: The URL to redirect to after a successful action.
    """
    request = context['request']

    if isinstance(survey, str):
        survey = Survey.objects.select_related('options').get(pk=survey)

    context.update({
        'survey': survey,
        'survey_json': {
            'title': survey.title,
            'description': survey.description,
            'start_date': str(survey.start_date),
            'end_date': str(survey.end_date),
            'options': list(survey.options.filter(is_active=True).values('title', 'color', 'vote_count')),
        },
        'show_title': show_title,
        'show_description': show_description,
        'show_image': show_image,
        'success_url': success_url,
        'row_class': row_class,
    })

    if request.user.is_authenticated:
        user_choices = request.user.survey_choices.all().select_related('option')
        context['user_choice'] = user_choices.filter(option__survey=survey).first()
        context['user_choices'] = user_choices

    return context