from django import forms

class UsernameForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        min_length=1,
        strip=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter GitHub username (e.g., octocat)',
            'autocomplete': 'off'
        }),
        help_text='Sample valid: octocat, torvalds. Invalid will show error.'
    )

    def clean_username(self):
        username = self.cleaned_data['username'].lower().strip()
        if not username or len(username) < 1:
            raise forms.ValidationError('Username cannot be empty.')
        if not all(c.isalnum() or c == '_' for c in username):
            raise forms.ValidationError('Username must contain only alphanumeric characters and underscores.')
        return username