from django.db import models
from apps.clients.models import Client
from apps.portfolios.models import Project

class PortfolioFile(models.Model):
    CATEGORY_CHOICES = [
        ('profile_image', 'Profile Image'),
        ('project_image', 'Project Image'),
        ('resume', 'Resume'),
        ('certificate', 'Certificate'),
        ('document', 'Document'),
        ('other', 'Other'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='files')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    
    display_title = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    
    # Cloudinary metadata
    cloudinary_public_id = models.CharField(max_length=255)
    cloudinary_url = models.URLField(max_length=1000, blank=True, default='')
    cloudinary_resource_type = models.CharField(max_length=50, default='image') # 'image' or 'raw'
    delivery_type = models.CharField(max_length=50, default='upload') # 'upload', 'authenticated', 'private'
    
    file_format = models.CharField(max_length=20) # jpg, png, pdf, docx, etc.
    verified_content_type = models.CharField(max_length=100)
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private', db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['client', 'visibility']),
            models.Index(fields=['client', 'category']),
            models.Index(fields=['cloudinary_public_id']),
        ]

    def __str__(self):
        return f"{self.display_title} ({self.client.name})"

    @property
    def file_size_display(self):
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"

    @property
    def is_image(self):
        return self.category in ['profile_image', 'project_image'] or self.file_format.lower() in ['jpg', 'jpeg', 'png', 'webp', 'gif']
