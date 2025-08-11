from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.sessions.models import Session

from .models import Survey, SurveyOption, SurveyChoice


User = get_user_model()


class SurveyAnonymousVotingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create survey that requires authentication
        self.auth_survey = Survey.objects.create(
            title='Auth Required Survey',
            description='This survey requires authentication',
            requires_authentication=True
        )
        self.auth_option1 = SurveyOption.objects.create(
            survey=self.auth_survey,
            title='Auth Option 1',
            color='#ff0000'
        )
        self.auth_option2 = SurveyOption.objects.create(
            survey=self.auth_survey,
            title='Auth Option 2',
            color='#00ff00'
        )
        
        # Create survey that allows anonymous voting
        self.anon_survey = Survey.objects.create(
            title='Anonymous Survey',
            description='This survey allows anonymous voting',
            requires_authentication=False
        )
        self.anon_option1 = SurveyOption.objects.create(
            survey=self.anon_survey,
            title='Anon Option 1',
            color='#0000ff'
        )
        self.anon_option2 = SurveyOption.objects.create(
            survey=self.anon_survey,
            title='Anon Option 2',
            color='#ffff00'
        )
        
        self.client = Client()

    def test_survey_default_requires_authentication(self):
        """Test that surveys require authentication by default."""
        default_survey = Survey.objects.create(title='Default Survey')
        self.assertTrue(default_survey.requires_authentication)

    def test_authenticated_user_can_vote_on_auth_required_survey(self):
        """Test that authenticated users can vote on surveys requiring authentication."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('survey:vote'), {
            'survey_option_id': self.auth_option1.pk,
            'success_url': '/',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SurveyChoice.objects.filter(
            option=self.auth_option1,
            user=self.user
        ).exists())

    def test_anonymous_user_cannot_vote_on_auth_required_survey(self):
        """Test that anonymous users cannot vote on surveys requiring authentication."""
        response = self.client.post(reverse('survey:vote'), {
            'survey_option_id': self.auth_option1.pk,
            'success_url': '/',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(SurveyChoice.objects.filter(
            option=self.auth_option1
        ).exists())

    def test_anonymous_user_can_vote_on_anonymous_survey(self):
        """Test that anonymous users can vote on surveys allowing anonymous voting."""
        # First request to establish session
        self.client.get(reverse('survey:survey_detail', kwargs={'pk': self.anon_survey.pk}))
        
        response = self.client.post(reverse('survey:vote'), {
            'survey_option_id': self.anon_option1.pk,
            'success_url': '/',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SurveyChoice.objects.filter(
            option=self.anon_option1,
            user__isnull=True
        ).exists())

    def test_authenticated_user_can_vote_on_anonymous_survey(self):
        """Test that authenticated users can also vote on anonymous surveys."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('survey:vote'), {
            'survey_option_id': self.anon_option1.pk,
            'success_url': '/',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SurveyChoice.objects.filter(
            option=self.anon_option1,
            user=self.user
        ).exists())

    def test_anonymous_user_cannot_vote_twice(self):
        """Test that anonymous users cannot vote twice on the same survey."""
        # First vote
        self.client.get(reverse('survey:survey_detail', kwargs={'pk': self.anon_survey.pk}))
        session_key = self.client.session.session_key
        
        # Create a vote manually to simulate first vote
        SurveyChoice.objects.create(
            option=self.anon_option1,
            session_key=session_key
        )
        
        # Try to vote again
        response = self.client.post(reverse('survey:vote'), {
            'survey_option_id': self.anon_option2.pk,
            'success_url': '/',
        })
        
        self.assertEqual(response.status_code, 302)
        # Should still have only one vote
        self.assertEqual(SurveyChoice.objects.filter(
            option__survey=self.anon_survey,
            session_key=session_key
        ).count(), 1)

    def test_authenticated_user_cannot_vote_twice(self):
        """Test that authenticated users cannot vote twice on the same survey."""
        self.client.login(username='testuser', password='testpass123')
        
        # First vote
        response = self.client.post(reverse('survey:vote'), {
            'survey_option_id': self.anon_option1.pk,
            'success_url': '/',
        })
        self.assertEqual(response.status_code, 302)
        
        # Try to vote again
        response = self.client.post(reverse('survey:vote'), {
            'survey_option_id': self.anon_option2.pk,
            'success_url': '/',
        })
        self.assertEqual(response.status_code, 302)
        
        # Should still have only one vote
        self.assertEqual(SurveyChoice.objects.filter(
            option__survey=self.anon_survey,
            user=self.user
        ).count(), 1)

    def test_survey_has_session_voted(self):
        """Test the has_session_voted method."""
        session_key = 'test_session_key'
        self.assertFalse(self.anon_survey.has_session_voted(session_key))
        
        SurveyChoice.objects.create(
            option=self.anon_option1,
            session_key=session_key
        )
        
        self.assertTrue(self.anon_survey.has_session_voted(session_key))

    def test_survey_get_user_choice_for_session(self):
        """Test getting user choice by session key."""
        session_key = 'test_session_key'
        choice = SurveyChoice.objects.create(
            option=self.anon_option1,
            session_key=session_key
        )
        
        retrieved_choice = self.anon_survey.get_user_choice(session_key=session_key)
        self.assertEqual(retrieved_choice, choice)

    def test_survey_choice_validation_user_or_session_required(self):
        """Test that SurveyChoice requires either user or session_key."""
        with self.assertRaises(ValidationError):
            choice = SurveyChoice(option=self.anon_option1)
            choice.clean()

    def test_survey_choice_str_method_for_anonymous(self):
        """Test string representation for anonymous votes."""
        choice = SurveyChoice.objects.create(
            option=self.anon_option1,
            session_key='test_session'
        )
        self.assertEqual(str(choice), 'Anonymous | Anon Option 1')

    def test_vote_count_updates_correctly(self):
        """Test that vote counts update correctly for both authenticated and anonymous votes."""
        # Initial counts
        self.assertEqual(self.anon_option1.vote_count, 0)
        self.assertEqual(self.anon_option2.vote_count, 0)
        
        # Add authenticated vote
        SurveyChoice.objects.create(option=self.anon_option1, user=self.user)
        self.anon_option1.update_vote_count()
        self.assertEqual(self.anon_option1.vote_count, 1)
        
        # Add anonymous vote
        SurveyChoice.objects.create(option=self.anon_option1, session_key='session1')
        self.anon_option1.update_vote_count()
        self.assertEqual(self.anon_option1.vote_count, 2)
        
        # Add another anonymous vote to different option
        SurveyChoice.objects.create(option=self.anon_option2, session_key='session2')
        self.anon_option2.update_vote_count()
        self.assertEqual(self.anon_option2.vote_count, 1)
