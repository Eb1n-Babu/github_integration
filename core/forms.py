from django import forms

class UsernameForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        min_length=1,
        strip=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter GitHub username (e.g., octocat or Eb1n-Babu)',
            'autocomplete': 'off'
        }),
        help_text='Sample valid: octocat, torvalds, Eb1n-Babu. Allows letters, digits, hyphens, underscores.'
    )

    def clean_username(self):
        username = self.cleaned_data['username'].lower().strip()
        if not username or len(username) < 1:
            raise forms.ValidationError('Username cannot be empty.')
        # Allows letters (a-zA-Z), digits (0-9), hyphens (-), underscores (_)
        if not all(c.isalnum() or c in '-_' for c in username):
            raise forms.ValidationError('Username must contain only letters, digits, hyphens, or underscores.')
        return username