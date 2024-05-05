

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Survey, SurveyOption, SurveyChoice


@receiver(post_save, sender=SurveyChoice)
def on_post_save_survey_choice(sender, instance: SurveyChoice, created, **kwargs):
    instance.option.survey.update_options()


@receiver(post_delete, sender=SurveyChoice)
def on_post_delete_survey_choice(sender, instance: SurveyChoice, **kwargs):
    instance.option.survey.update_options()