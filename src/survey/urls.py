
from django.urls import path

from .views import (
    SurveyDetailView,
    vote_view,
)


app_name = 'survey'

urlpatterns = [
    path('<uuid:pk>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('vote/', vote_view, name='vote'),
]
