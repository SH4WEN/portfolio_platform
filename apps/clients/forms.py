from django import forms
from apps.clients.models import Client

_INPUT_CLASS = (
    'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 '
    'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 '
    'focus:ring-2 focus:ring-cyan-500 focus:outline-none transition'
)

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name', 'email', 'profession', 'headline', 'bio',
            'portfolio_style',
            'profile_image_url',
            'github_url', 'linkedin_url', 'website_url',
            'twitter_url', 'instagram_url', 'facebook_url',
            'youtube_url', 'tiktok_url',
            'phone', 'location', 'is_published',
        ]
        widgets = {
            'name':              forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'e.g. Sherwin Sarmiento'}),
            'email':             forms.EmailInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'client@example.com'}),
            'profession':        forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'e.g. Senior Full-Stack Engineer'}),
            'headline':          forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'e.g. Building scalable web solutions & cloud systems'}),
            'bio':               forms.Textarea(attrs={'class': _INPUT_CLASS, 'rows': 4, 'placeholder': 'Write client professional summary...'}),
            'portfolio_style':   forms.Select(attrs={'class': _INPUT_CLASS}),
            'profile_image_url': forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://...'}),
            'github_url':        forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://github.com/username'}),
            'linkedin_url':      forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://linkedin.com/in/username'}),
            'website_url':       forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://yourwebsite.com'}),
            'twitter_url':       forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://x.com/username'}),
            'instagram_url':     forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://instagram.com/username'}),
            'facebook_url':      forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://facebook.com/username'}),
            'youtube_url':       forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://youtube.com/@username'}),
            'tiktok_url':        forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://tiktok.com/@username'}),
            'phone':             forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': '+1 234 567 890'}),
            'location':          forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'San Francisco, CA'}),
            'is_published':      forms.CheckboxInput(attrs={'class': 'w-5 h-5 rounded border-gray-300 text-cyan-600 focus:ring-cyan-500 bg-white dark:bg-gray-800 dark:border-gray-700'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Every field on the client form is optional — no submission requires input.
        for field in self.fields.values():
            field.required = False

    def _clean_social_url(self, field_name, base_url):
        val = self.cleaned_data.get(field_name, '').strip()
        if not val:
            return ''
        if val.startswith(('http://', 'https://')):
            return val
        # Handle handles starting with @ or domain
        val = val.lstrip('@')
        if '/' in val and base_url.replace('https://', '') in val:
            return f"https://{val}"
        return f"{base_url}{val}"

    def clean_github_url(self):
        return self._clean_social_url('github_url', 'https://github.com/')

    def clean_linkedin_url(self):
        return self._clean_social_url('linkedin_url', 'https://linkedin.com/in/')

    def clean_twitter_url(self):
        return self._clean_social_url('twitter_url', 'https://x.com/')

    def clean_instagram_url(self):
        return self._clean_social_url('instagram_url', 'https://instagram.com/')

    def clean_facebook_url(self):
        return self._clean_social_url('facebook_url', 'https://facebook.com/')

    def clean_youtube_url(self):
        return self._clean_social_url('youtube_url', 'https://youtube.com/')

    def clean_tiktok_url(self):
        val = self.cleaned_data.get('tiktok_url', '').strip()
        if not val:
            return ''
        if val.startswith(('http://', 'https://')):
            return val
        val = val.lstrip('@')
        return f"https://tiktok.com/@{val}"

