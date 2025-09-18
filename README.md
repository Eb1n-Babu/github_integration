# GitHub API Integration - Django App

[![Python](https://img.shields.io/badge/Python-3.13.3-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0.4-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django web application that integrates with the GitHub Public API (no authentication required) to fetch and analyze user repository data. Uses SQLite for database persistence.

## Description
This app handles user profile fetching, repository analysis, and data retrieval from the database. It supports valid and invalid usernames with meaningful error messages.

API Details:
- User API: `https://api.github.com/users/<username>` (e.g., `/users/octocat`).
- Repo API: `https://api.github.com/users/<username>/repos` (e.g., `/users/octocat/repos`).

Sample Valid Usernames: octocat, torvalds, JakeWharton, mojombo, pjhyett, Eb1n-Babu.
Sample Invalid Usernames: thisuserdoesnotexist12345, invalid_account_xyz, notarealuser_999, fake_github_user_test, ghost123fake.

## Key Features
- **User Profile Fetching**: Input GitHub username (e.g., "octocat"), fetch and display name, public repos count, followers & following, account creation date. Saves to SQLite DB.
- **Repository Analysis**: Fetches all repos, displays name, primary language, star count, fork count, last updated date.
- **Fetch from DB**: Input username, retrieves and displays saved profile fields from DB.
- **Error Handling**: Handles invalid usernames (404) with meaningful messages.

## Installation
1. **Clone/Setup Project**:

git clone <repo-url> github_integration
cd github_integration
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt</repo-url>


2. **Database Setup** (SQLite):

python manage.py makemigrations core
python manage.py migrate

3. **Run Server**

python manage.py runserver

- Access: http://127.0.0.1:8000/ (Fetch Profile form).

## Usage
1. **Fetch Profile & Repos** (`/`):
- Enter username (e.g., "octocat" or "Eb1n-Babu").
- Displays profile (name, repos count, followers/following, created date).
- Lists repos (name, language, stars, forks, updated).
- Saves to SQLite (`db.sqlite3`).

2. **Fetch from DB** (`/fetch_db/`):
- Enter saved username (e.g., "octocat").
- Displays saved fields (name, repos count, followers/following, created date).

3. **Error Example**:
- Enter "thisuserdoesnotexist12345" → "User 'thisuserdoesnotexist12345' not found (invalid username)."

## Testing

python manage.py test core

- Output: `Ran 7 tests in X.XXXs OK` (covers valid/invalid samples, API mocks, DB ops, validation; testing still in progress).

## Deployment (Docker - SQLite Only)
1. **Build Image**:
docker build -t github-integration-django:v1.0.0 .

2. **Start Container** (SQLite persists via volume):
docker run -d --name github-app -p 8000:8000 -v "%CD%/db.sqlite3:/app/db.sqlite3" github-integration-django:v1.0.0


3. **Access**: http://localhost:8000.
4. **Stop**: `docker stop github-app && docker rm github-app`.

Prod Tips: Set `DEBUG=False` in env, use Gunicorn (`CMD ["gunicorn", "github_integration.wsgi"]` in Dockerfile), Nginx reverse proxy (Docker implementation in progress).

## Contributing
- Fork, branch, commit with conventional messages (e.g., "feat: add hyphen validation").
- Test: `python manage.py test core`.
- Pull request with description.

## License
MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments
- Dependencies: Django 5.0.4, requests 2.32.3.
- UI: Bootstrap 5 CDN.

---

**Current Version**: v1.0.0 (SQLite, Docker-ready). Questions? Open an issue!

docker build --no-cache -t github-integration-django:v1.0.0 .
docker run -d --name github-app -p 8000:8000 github-integration-django:v1.0.0
