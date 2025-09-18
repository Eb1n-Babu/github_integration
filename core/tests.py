from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from .models import GitHubUser
from datetime import datetime, timezone
import requests
import warnings

VALID_USERNAMES = ['octocat', 'torvalds', 'JakeWharton', 'mojombo', 'pjhyett', 'Eb1n-Babu']  # Includes hyphen/numeric valid
INVALID_USERNAMES = ['thisuserdoesnotexist12345', 'invalid_account_xyz', 'notarealuser_999', 'fake_github_user_test', 'ghost123fake']

class GitHubIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_fetch_profile_valid_usernames(self):
        """Test fetching and displaying profile/repos for all valid sample usernames; save to DB."""
        mock_profile = {
            'name': 'Test User',
            'public_repos': 10,
            'followers': 100,
            'following': 50,
            'created_at': '2011-10-05T20:59:09Z'
        }
        mock_repos = [
            {'name': 'TestRepo', 'language': 'Python', 'stargazers_count': 5, 'forks_count': 2, 'updated_at': '2023-01-01T00:00:00Z'}
        ]

        for username in VALID_USERNAMES:
            with patch('requests.get') as mock_get:
                mock_get.side_effect = [
                    MagicMock(status_code=200, json=lambda: mock_profile),
                    MagicMock(status_code=200, json=lambda: mock_repos)
                ]
                response = self.client.post(reverse('core:fetch_profile'), {'username': username})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Test User')  # Name
                self.assertContains(response, '10')  # Public repos
                self.assertContains(response, '100')  # Followers
                self.assertContains(response, '50')  # Following
                self.assertContains(response, '2011-10-05T20:59:09Z')  # Created date
                self.assertContains(response, 'TestRepo')  # Repo name
                self.assertContains(response, 'Python')  # Language
                self.assertContains(response, '5')  # Stars
                self.assertContains(response, '2')  # Forks
                self.assertContains(response, '2023-01-01T00:00:00Z')  # Updated
                # Verify save branch taken (success message)
                lowered_username = username.lower()
                self.assertContains(response, f"Data for {lowered_username} fetched and saved successfully!")

            # DB verify (lowered)
            lowered_username = username.lower()
            user = GitHubUser.objects.get(username=lowered_username)
            self.assertEqual(user.name, 'Test User')

    def test_fetch_profile_invalid_usernames(self):
        """Test error handling and meaningful messages for all invalid sample usernames (404)."""
        for username in INVALID_USERNAMES:
            with patch('requests.get') as mock_get:
                mock_get.return_value.status_code = 404
                response = self.client.post(reverse('core:fetch_profile'), {'username': username})
                self.assertEqual(response.status_code, 200)
                # Exact raw HTML match (&#x27; for ', period)
                escaped_msg = f"User &#x27;{username}&#x27; not found (invalid username)."
                self.assertContains(response, escaped_msg, html=False)

    def test_fetch_from_db_valid(self):
        """Test fetching and displaying profile fields from DB for saved user."""
        username = 'octocat'
        lowered_username = username.lower()
        created_at = datetime(2023, 1, 1, tzinfo=timezone.utc)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            GitHubUser.objects.create(
                username=lowered_username,
                name='Saved Name',
                public_repos=20,
                followers=200,
                following=100,
                created_at=created_at
            )
        response = self.client.post(reverse('core:fetch_db'), {'username': username})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Saved Name')  # Name
        self.assertContains(response, '20')  # Public repos
        self.assertContains(response, '200')  # Followers
        self.assertContains(response, '100')  # Following
        self.assertContains(response, '2023-01-01T00:00:00')  # Created date

    def test_fetch_from_db_invalid(self):
        """Test no data found in DB with meaningful message."""
        username = 'nonexistent'
        response = self.client.post(reverse('core:fetch_db'), {'username': username})
        self.assertEqual(response.status_code, 200)
        # Exact raw HTML match (&#x27; for ', period)
        escaped_msg = f"No data found for &#x27;{username}&#x27; in database."
        self.assertContains(response, escaped_msg, html=False)

    def test_form_validation(self):
        """Test form input validation."""
        response = self.client.post(reverse('core:fetch_profile'), {'username': ''})
        self.assertContains(response, "This field is required.")

        response = self.client.post(reverse('core:fetch_profile'), {'username': 'invalid@chars'})
        self.assertContains(response, 'Username must contain only letters, digits, hyphens, or underscores.')

    @patch('requests.get')
    def test_api_rate_limit_error(self, mock_get):
        """Test handling API rate limit (403) with meaningful message."""
        mock_get.return_value.status_code = 403
        response = self.client.post(reverse('core:fetch_profile'), {'username': 'octocat'})
        self.assertContains(response, 'API rate limit exceeded')

    @patch('requests.get')
    def test_api_timeout_error(self, mock_get):
        """Test handling timeout with meaningful message."""
        mock_get.side_effect = requests.exceptions.Timeout
        response = self.client.post(reverse('core:fetch_profile'), {'username': 'octocat'})
        self.assertContains(response, 'Request timed out.')