# README.md
# GitHub API Integration - Django App

A Django web application for fetching and analyzing GitHub user data via Public API.

## Quick Start
1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py runserver`
4. Visit `http://127.0.0.1:8000/`

## Features
- Fetch user profile and repos
- Save to DB (SQLite/MySQL)
- Retrieve from DB
- Error handling for invalid users
- Responsive UI with Bootstrap

## Testing
`python manage.py test core`

## Deployment
- Set `DJANGO_DEBUG=False`
- Configure DATABASES for MySQL
- `python manage.py collectstatic`
- Use gunicorn/nginx

## Samples
Valid: octocat, torvalds
Invalid: thisuserdoesnotexist12345

# Setup Commands:
# git init
# git add .
# git commit -m "Initial commit: Initialize Git repository for Django-based GitHub API Integration application, including project structure, requirements, and setup instructions"
# django-admin startproject github_integration .
# cd github_integration
# python manage.py startapp core
# (Add 'core' to INSTALLED_APPS in settings.py)
# python manage.py makemigrations core
# python manage.py migrate
# python manage.py test core
# python manage.py runserver