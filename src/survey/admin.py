from django.contrib import admin

from .models import Survey, SurveyOption, SurveyChoice


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'create_date',
    )
    readonly_fields = (
        'create_date',
        'create_user',
        'update_date',
        'update_user',
    )


@admin.register(SurveyOption)
class SurveyOptionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'create_date',
        'vote_count',
    )
    readonly_fields = (
        'vote_count',
        'create_date',
        'create_user',
        'update_date',
        'update_user',
    )


@admin.register(SurveyChoice)
class SurveyChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'option',
    )
    readonly_fields = (
        'user',
        'option',
        'create_date',
        'create_user',
        'update_date',
        'update_user',
    )