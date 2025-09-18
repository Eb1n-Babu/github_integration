# GitHub API Integration - Django App

[![Python](https://img.shields.io/badge/Python-3.13.3-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0.4-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django web application that integrates with the GitHub Public API (no authentication required) to 
fetch and analyze user repository data. Uses SQLite for database persistence.

## Description
This app handles user profile fetching, repository analysis, and data retrieval from the database.
It supports valid and invalid usernames with meaningful error messages.

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

git clone git remote add origin https://github.com/Eb1n-Babu/github_integration.git
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
docker build --no-cache -t github-integration-django:v1.0.0 .

2. **Start Container** (SQLite persists via volume):
docker run -d --name github-app -p 8000:8000 github-integration-django:v1.0.0


3. **Access**: http://localhost:8000.
4. **Stop**: `docker stop github-app && docker rm github-app`.

Prod Tips: Set `DEBUG=False` in env, use Gunicorn (`CMD ["gunicorn", "github_integration.wsgi"]` in Dockerfile), Nginx reverse proxy (Docker implementation in progress).

**Sharing Your Dockerized GitHub API Django App**

**How to Access the Shared App**

**Prerequisites:**

Docker installed (docker.com).
Docker Hub account (free; login if private repo).


**Pull the Image** 
docker pull ebinbabu/github-integration-django:v1.0.0

https://hub.docker.com/repository/docker/ebinbabu/github-integration-django

Expected: Downloads ~150MB image in ~1 min.
Verify: docker images | findstr github-integration-django.


**Run the Container (SQLite persists via volume; access at http://localhost:8000):**
docker run -d --name github-app -p 8000:8000  ebinbabu/github-integration-django:v1.0.0

Flags:

-d: Run in background.
--name github-app: Container name.
-p 8000:8000: Maps port (access UI at http://localhost:8000).


Expected: Starts server; logs: docker logs github-app → "Starting development server at http://0.0.0.0:8000/".
Verify: docker ps → "github-app Up".


Access the App:

URL: http://localhost:8000 (Bootstrap UI loads).
Test Profile Fetch: Enter "octocat" → Displays name ("The Octocat"), repos count (8), followers (0), following (0), created date ("2011-10-05T20:59:09Z"); lists repos (e.g., "Hello-World", language "N/A", stars 1).
Test DB Fetch: http://localhost:8000/fetch_db/ → Enter "octocat" → Shows saved fields.
Test Invalid: Enter "thisuserdoesnotexist12345" → "User 'thisuserdoesnotexist12345' not found (invalid username)."


Stop & Clean:
docker stop github-app
docker rm github-app

**Production Tips:**

Set DEBUG=False via env var (-e DEBUG=False in docker run) for HSTS/SSL.
Use Gunicorn: Update Dockerfile CMD to ["gunicorn", "github_integration.wsgi", "--bind", "0.0.0.0:8000"].
Add Nginx reverse proxy for HTTPS/static serving.
Push to Docker Hub: docker tag ... yourusername/repo:v1.0.0 && docker push yourusername/repo:v1.0.0.

**Contributing**

Fork the repository.
Create a branch: git checkout -b feature/new-feature.
Commit changes: git commit -m "feat: add new feature".
Push: git push origin feature/new-feature.
Open a Pull Request.

Use conventional commits (e.g., "feat:", "fix:", "docs:").

**License**
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

**Thanks to the Django and Bootstrap communities for the robust tools.**
Inspired by GitHub's Public API documentation.
Special thanks to contributors and testers for feedback.