from django import forms

from .models import SurveyChoice



class SurveyChoiceForm(forms.ModelForm):
    class Meta:
        model = SurveyChoice
        fields = (
            'option',
            'user',
        )