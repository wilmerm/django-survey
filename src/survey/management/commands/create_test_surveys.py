from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from survey.models import Survey, SurveyOption

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test surveys for manual testing'

    def handle(self, *args, **options):
        # Create test user if not exists
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Created test user: {user.username}')
        
        # Create survey that requires authentication
        auth_survey, created = Survey.objects.get_or_create(
            title='Authentication Required Survey',
            defaults={
                'description': 'This survey requires users to be logged in to vote.',
                'requires_authentication': True,
                'create_user': user
            }
        )
        if created:
            SurveyOption.objects.create(
                survey=auth_survey,
                title='Option A (Auth Required)',
                description='This is option A',
                color='#ff0000',
                create_user=user
            )
            SurveyOption.objects.create(
                survey=auth_survey,
                title='Option B (Auth Required)', 
                description='This is option B',
                color='#00ff00',
                create_user=user
            )
            self.stdout.write(f'Created auth survey: {auth_survey.title}')
        
        # Create survey that allows anonymous voting
        anon_survey, created = Survey.objects.get_or_create(
            title='Anonymous Voting Survey',
            defaults={
                'description': 'This survey allows anonymous users to vote. No login required!',
                'requires_authentication': False,
                'create_user': user
            }
        )
        if created:
            SurveyOption.objects.create(
                survey=anon_survey,
                title='Option X (Anonymous OK)',
                description='This is option X',
                color='#0000ff',
                create_user=user
            )
            SurveyOption.objects.create(
                survey=anon_survey,
                title='Option Y (Anonymous OK)',
                description='This is option Y', 
                color='#ffff00',
                create_user=user
            )
            SurveyOption.objects.create(
                survey=anon_survey,
                title='Option Z (Anonymous OK)',
                description='This is option Z',
                color='#ff00ff',
                create_user=user
            )
            self.stdout.write(f'Created anonymous survey: {anon_survey.title}')
        
        self.stdout.write('Test surveys created successfully!')
        self.stdout.write(f'Auth survey URL: http://127.0.0.1:8000/survey/{auth_survey.pk}/')
        self.stdout.write(f'Anonymous survey URL: http://127.0.0.1:8000/survey/{anon_survey.pk}/')
        self.stdout.write('Admin URL: http://127.0.0.1:8000/admin/')
        self.stdout.write('Test user: testuser / testpass123')
        self.stdout.write('Admin user: admin / (no password set)')