import requests
from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import request

from .models import GitHubUser
from .forms import UsernameForm

@method_decorator(csrf_protect, name='dispatch')
class FetchProfileView(View):
    template_name = 'core/fetch_profile.html'
    form_class = UsernameForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            profile_data, repos_data, error = self.fetch_github_data(username)
            if error:
                messages.error(request, error)
                return render(request, self.template_name, {'form': form})
            # Save to DB
            created_at = None
            if profile_data['created_at'] != 'N/A':
                created_at_str = profile_data['created_at'].replace('Z', '+00:00')
                created_at = datetime.fromisoformat(created_at_str)
            GitHubUser.objects.update_or_create(
                username=username,
                defaults={
                    'name': profile_data['name'],
                    'public_repos': profile_data['public_repos'],
                    'followers': profile_data['followers'],
                    'following': profile_data['following'],
                    'created_at': created_at
                }
            )
            messages.success(request, f"Data for {username} fetched and saved successfully!")
            return render(request, 'core/results_profile.html', {
                'username': username,
                'profile': profile_data,
                'repos': repos_data
            })
        return render(request, self.template_name, {'form': form})

    def fetch_github_data(self, username):
        try:
            # User profile
            user_url = f"https://api.github.com/users/{username}"
            user_resp = requests.get(user_url, timeout=10)
            if user_resp.status_code == 404:
                return None, None, f"User '{username}' not found (invalid username)."
            if user_resp.status_code == 403:
                return None, None, "API rate limit exceeded (60 requests/hour unauthenticated). Try again later."
            if user_resp.status_code != 200:
                return None, None, f"Error fetching profile: HTTP {user_resp.status_code}"

            data = user_resp.json()
            profile_data = {
                'name': data.get('name', 'N/A'),
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'created_at': data.get('created_at', 'N/A')
            }

            # Repositories
            repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
            repos_resp = requests.get(repos_url, timeout=10)
            repos = []
            if repos_resp.status_code == 200:
                repos_data_json = repos_resp.json()
                for repo in repos_data_json:
                    repos.append({
                        'name': repo.get('name', 'N/A'),
                        'language': repo.get('language', 'N/A'),
                        'stars': repo.get('stargazers_count', 0),
                        'forks': repo.get('forks_count', 0),
                        'updated_at': repo.get('updated_at', 'N/A')
                    })
            elif repos_resp.status_code != 404:
                messages.warning(request, f"Could not fetch repositories: HTTP {repos_resp.status_code}")

            return profile_data, repos, None
        except requests.exceptions.Timeout:
            return None, None, "Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return None, None, f"API connection error: {str(e)}"
        except (ValueError, KeyError) as e:
            return None, None, f"Invalid API response: {str(e)}"
        except Exception as e:
            return None, None, f"Unexpected error: {str(e)}"

@method_decorator(csrf_protect, name='dispatch')
class FetchFromDBView(View):
    template_name = 'core/fetch_db.html'
    form_class = UsernameForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = GitHubUser.objects.get(username=username)
                db_data = {
                    'name': user.name or 'N/A',
                    'public_repos': user.public_repos,
                    'followers': user.followers,
                    'following': user.following,
                    'created_at': user.created_at.isoformat() if user.created_at else 'N/A'
                }
                return render(request, 'core/results_db.html', {
                    'username': username,
                    'data': db_data
                })
            except GitHubUser.DoesNotExist:
                messages.error(request, f"No data found for '{username}' in database.")
        return render(request, self.template_name, {'form': form})