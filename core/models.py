from django.db import models

class GitHubUser(models.Model):
    username = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    public_repos = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'github_users'
        verbose_name = 'GitHub User'
        verbose_name_plural = 'GitHub Users'

