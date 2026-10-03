from django import forms
from apps.media_manager.models import PortfolioFile
from apps.clients.models import Client
from apps.portfolios.models import Project

class PortfolioFileUploadForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'})
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'})
    )
    display_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'e.g. Executive Resume 2026 / Project Architecture Diagram'})
    )
    category = forms.ChoiceField(
        choices=PortfolioFile.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'})
    )
    visibility = forms.ChoiceField(
        choices=PortfolioFile.VISIBILITY_CHOICES,
        initial='private',
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'})
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-cyan-500 file:text-white hover:file:bg-cyan-600 cursor-pointer'})
    )


class PortfolioFileReplaceForm(forms.Form):
    display_title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'})
    )
    visibility = forms.ChoiceField(
        choices=PortfolioFile.VISIBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'})
    )
    file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-cyan-500 file:text-white hover:file:bg-cyan-600 cursor-pointer'})
    )
