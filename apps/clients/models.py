from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Client(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    email = models.EmailField()
    profession = models.CharField(max_length=255)
    headline = models.CharField(max_length=500)
    bio = models.TextField()
    
    # Profile media & social links
    profile_image_url = models.URLField(max_length=1000, blank=True, default='')
    github_url = models.URLField(max_length=500, blank=True, default='')
    linkedin_url = models.URLField(max_length=500, blank=True, default='')
    website_url = models.URLField(max_length=500, blank=True, default='')
    twitter_url = models.URLField(max_length=500, blank=True, default='')
    instagram_url = models.URLField(max_length=500, blank=True, default='')
    facebook_url = models.URLField(max_length=500, blank=True, default='')
    youtube_url = models.URLField(max_length=500, blank=True, default='')
    tiktok_url = models.URLField(max_length=500, blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    
    # Status & Timestamps
    is_published = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portfolios:public_portfolio', kwargs={'slug': self.slug})

    def generate_unique_slug(self):
        base_slug = slugify(self.name) or "client"
        slug = base_slug
        count = 1
        while Client.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Client.objects.filter(pk=self.pk, name=self.name).exists() is False):
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
