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
            'profile_image_url': forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://...'}),
            'github_url':        forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://github.com/username'}),
            'linkedin_url':      forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://linkedin.com/in/username'}),
            'website_url':       forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://yourwebsite.com'}),
            'twitter_url':       forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://x.com/username'}),
            'instagram_url':     forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://instagram.com/username'}),
            'facebook_url':      forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://facebook.com/username'}),
            'youtube_url':       forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://youtube.com/@channel'}),
            'tiktok_url':        forms.URLInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'https://tiktok.com/@username'}),
            'phone':             forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': '+1 234 567 890'}),
            'location':          forms.TextInput(attrs={'class': _INPUT_CLASS, 'placeholder': 'San Francisco, CA'}),
            'is_published':      forms.CheckboxInput(attrs={'class': 'w-5 h-5 rounded border-gray-300 text-cyan-600 focus:ring-cyan-500 bg-white dark:bg-gray-800 dark:border-gray-700'}),
        }
