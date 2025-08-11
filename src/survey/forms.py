from django import forms

from .models import SurveyChoice


class SurveyChoiceForm(forms.ModelForm):
    class Meta:
        model = SurveyChoice
        fields = (
            'option',
            'user',
            'session_key',
        )

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        session_key = cleaned_data.get('session_key')
        
        # Ensure either user or session_key is provided, but not both
        if user and session_key:
            raise forms.ValidationError("Cannot have both user and session_key.")
        if not user and not session_key:
            raise forms.ValidationError("Either user or session_key must be provided.")
            
        return cleaned_data