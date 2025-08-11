from django.contrib import admin

from .models import Survey, SurveyOption, SurveyChoice


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'requires_authentication',
        'create_date',
        'is_active',
    )
    list_filter = (
        'requires_authentication',
        'is_active',
        'create_date',
    )
    readonly_fields = (
        'create_date',
        'create_user',
        'update_date',
        'update_user',
    )
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'requires_authentication')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Display Options', {
            'fields': ('options_cssclass',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System Information', {
            'fields': ('create_date', 'create_user', 'update_date', 'update_user'),
            'classes': ('collapse',)
        })
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
        'get_voter',
        'option',
        'create_date',
    )
    list_filter = (
        'option__survey',
        'create_date',
    )
    readonly_fields = (
        'user',
        'session_key',
        'option',
        'create_date',
        'create_user',
        'update_date',
        'update_user',
    )

    def get_voter(self, obj):
        return obj.user if obj.user else f"Anonymous ({obj.session_key[:8]}...)" if obj.session_key else "Unknown"
    get_voter.short_description = 'Voter'