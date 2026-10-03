from django import forms
from apps.portfolios.models import Project, Skill, Experience, Education

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'client', 'title', 'description', 'featured_image_url',
            'tech_stack', 'project_url', 'github_url', 'order', 'is_published'
        ]
        widgets = {
            'client': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'}),
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'rows': 4, 'placeholder': 'Describe project features, architecture, and impact...'}),
            'featured_image_url': forms.URLInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'https://...'}),
            'tech_stack': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'Python, Django, PostgreSQL, Tailwind'}),
            'project_url': forms.URLInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'https://demo.example.com'}),
            'github_url': forms.URLInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'https://github.com/...'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'w-5 h-5 rounded border-gray-300 text-cyan-600 focus:ring-cyan-500'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['client', 'name', 'category', 'proficiency', 'order']
        widgets = {
            'client': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'}),
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'e.g. Python'}),
            'category': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'e.g. Backend, Frontend, DevOps'}),
            'proficiency': forms.NumberInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'min': 0, 'max': 100}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['client', 'job_title', 'company', 'description', 'start_date', 'end_date', 'is_current']
        widgets = {
            'client': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'}),
            'job_title': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'Senior Developer'}),
            'company': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'Acme Corp'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'rows': 4, 'placeholder': 'Role highlights and responsibilities...'}),
            'start_date': forms.DateInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'w-5 h-5 rounded border-gray-300 text-cyan-600 focus:ring-cyan-500'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['client', 'institution', 'degree', 'description', 'start_date', 'end_date']
        widgets = {
            'client': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500'}),
            'institution': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'University Name'}),
            'degree': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'placeholder': 'B.S. Computer Science'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'rows': 3, 'placeholder': 'Honors, thesis, activities...'}),
            'start_date': forms.DateInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-cyan-500', 'type': 'date'}),
        }
