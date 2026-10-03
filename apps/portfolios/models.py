from django.db import models
from django.utils.text import slugify
from apps.clients.models import Client

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    featured_image_url = models.URLField(max_length=1000, blank=True, default='')
    tech_stack = models.CharField(max_length=500, help_text="Comma-separated skills/technologies e.g. Python, Django, Tailwind")
    project_url = models.URLField(max_length=500, blank=True, default='')
    github_url = models.URLField(max_length=500, blank=True, default='')
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        unique_together = ('client', 'slug')
        indexes = [
            models.Index(fields=['client', 'is_published']),
            models.Index(fields=['client', 'slug']),
        ]

    def __str__(self):
        return f"{self.title} ({self.client.name})"

    def generate_unique_slug(self):
        base_slug = slugify(self.title) or "project"
        slug = base_slug
        count = 1
        while Project.objects.filter(client=self.client, slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Project.objects.filter(pk=self.pk, title=self.title).exists() is False):
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    @property
    def tech_list(self):
        if not self.tech_stack:
            return []
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]


class Skill(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default='General', help_text="e.g. Frontend, Backend, DevOps, Languages")
    proficiency = models.PositiveIntegerField(default=80, help_text="Proficiency percentage 0-100")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'category', 'name']
        indexes = [
            models.Index(fields=['client', 'category']),
        ]

    def __str__(self):
        return f"{self.name} - {self.client.name}"


class Experience(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['client', '-start_date']),
        ]

    def __str__(self):
        return f"{self.job_title} at {self.company} ({self.client.name})"


class Education(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['client', '-start_date']),
        ]

    def __str__(self):
        return f"{self.degree} - {self.institution} ({self.client.name})"
