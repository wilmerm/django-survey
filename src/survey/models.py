import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _, gettext_lazy as _l

from colorfield.fields import ColorField


User = get_user_model()


class BaseModel(models.Model):
    create_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    update_date = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    create_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='%(class)s_created',
        null=True,
        blank=True,
        editable=False,
    )
    update_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='%(class)s_updated',
        null=True,
        blank=True,
        editable=False,
    )
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        abstract = True


class Survey(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=100,
    )
    description = models.CharField(
        max_length=500,
    )
    start_date = models.DateField(
        null=True,
    )
    end_date = models.DateField(
        null=True,
    )
    options_cssclass = models.CharField(
        max_length=500,
        default='col-sm-6 col-md-4 col-lg-3 col-xl-2',
    )

    def __str__(self):
        return self.title

    def update_options(self):
        for option in self.options.all():
            option.update_vote_count()

    def has_user_voted(self, user):
        return SurveyChoice.objects.filter(option__survey=self, user=user).exists()


class SurveyOption(BaseModel):
    survey = models.ForeignKey(
        Survey,
        related_name='options',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=100,
    )
    description = models.CharField(
        max_length=500,
    )
    vote_count = models.PositiveIntegerField(
        default=0,
        editable=False,
    )
    vote_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        editable=False,
    )
    image = models.ImageField(
        upload_to='survey/',
        null=True,
        blank=True,
    )
    color = ColorField(
        default='#FFFFFF',
    )

    def __str__(self):
        return self.title

    def update_vote_count(self, commit=True):
        self.vote_count = self.choices.all().count()

        total_votes = self.survey.options.aggregate(s=models.Count('choices'))['s']
        self.vote_percentage = (self.vote_count / total_votes) * 100 if total_votes else 0

        if commit:
            self.save()


class SurveyChoice(BaseModel):
    option = models.ForeignKey(
        SurveyOption,
        related_name='choices',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='survey_choices',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user} | {self.option}'

    def save(self, *args, **kwargs):
        self.validate_survey_is_active()
        self.validate_unique_user_survey_choice()
        super().save(*args, **kwargs)

    def clean(self):
        self.validate_survey_is_active()
        self.validate_unique_user_survey_choice()

    def validate_survey_is_active(self):
        if not self.option.survey.is_active:
            raise ValidationError(_('The survey is no longer active.'))

    def validate_unique_user_survey_choice(self):
        if self.option.survey.has_user_voted(self.user):
            raise ValidationError(_('You have already voted.'))
