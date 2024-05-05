from django.urls import path, include
from django.contrib import admin

from .views import index_view


urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin.site.urls),
    path('survey/', include('survey.urls')),
]