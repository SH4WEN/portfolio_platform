import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.clients.models import Client
from apps.portfolios.models import Project, Skill, Experience, Education
from apps.media_manager.models import PortfolioFile
from django.contrib.auth.models import User

def seed():
    # 1. Ensure admin superuser exists
    admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True})
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Created default admin user: admin / admin123")

    # 2. Create sample published client: Sherwin Sarmiento
    client, created = Client.objects.get_or_create(
        name="Sherwin Sarmiento",
        defaults={
            'email': 'sherwin@example.com',
            'profession': 'Senior Full-Stack Engineer & Cloud Architect',
            'headline': 'Building enterprise web applications, cloud infrastructure, and AI systems',
            'bio': 'Passionate senior software engineer with 8+ years of experience designing robust multi-tenant platforms, REST APIs, and modern responsive user interfaces.',
            'github_url': 'https://github.com/sh4wen',
            'linkedin_url': 'https://linkedin.com/in/sherwin-sarmiento',
            'website_url': 'https://sherwinsarmiento.dev',
            'location': 'San Francisco, CA',
            'is_published': True
        }
    )
    if created:
        print(f"Created sample client: {client.name} (slug: {client.slug})")

    # 3. Add Sample Projects
    Project.objects.get_or_create(
        client=client,
        title="Multi-Client Portfolio Platform",
        defaults={
            'description': 'A multi-tenant Django SaaS application enabling administrators to manage, publish, and host bespoke client portfolios with Cloudinary media integration and Neon PostgreSQL.',
            'tech_stack': 'Python, Django 5.2, PostgreSQL, Cloudinary, Tailwind CSS',
            'github_url': 'https://github.com/sh4wen/portfolio_platform',
            'order': 1,
            'is_published': True
        }
    )

    Project.objects.get_or_create(
        client=client,
        title="Enterprise Cloud Analytics Dashboard",
        defaults={
            'description': 'Real-time telemetry and metrics visualization portal with role-based access control and live data streaming.',
            'tech_stack': 'React, Python, Redis, WebSockets, Docker',
            'order': 2,
            'is_published': True
        }
    )

    # 4. Add Sample Skills
    skills = [
        ('Python & Django', 'Backend', 95, 1),
        ('PostgreSQL / Neon', 'Database', 90, 2),
        ('Tailwind CSS & JavaScript', 'Frontend', 88, 3),
        ('Cloudinary & AWS S3', 'Media & Storage', 85, 4),
        ('Docker & CI/CD Pipelines', 'DevOps', 85, 5),
    ]

    for name, cat, prof, order in skills:
        Skill.objects.get_or_create(
            client=client,
            name=name,
            defaults={'category': cat, 'proficiency': prof, 'order': order}
        )

    # 5. Add Sample Experience
    Experience.objects.get_or_create(
        client=client,
        job_title="Lead Software Engineer",
        company="TechCorp Solutions",
        defaults={
            'description': 'Architected high-throughput microservices and managed a team of 6 engineers building multi-tenant SaaS products.',
            'start_date': '2021-06-01',
            'is_current': True
        }
    )

    # 6. Add Sample Education
    Education.objects.get_or_create(
        client=client,
        institution="University of Technology",
        degree="B.S. Computer Science",
        defaults={
            'description': 'Graduated with Honors. Specialization in Software Engineering and Distributed Systems.',
            'start_date': '2015-08-01',
            'end_date': '2019-05-30'
        }
    )

    # 7. Add Sample Verified Public Certificate / File
    PortfolioFile.objects.get_or_create(
        client=client,
        display_title="AWS Certified Solutions Architect",
        defaults={
            'original_filename': 'aws_cert_2026.pdf',
            'category': 'certificate',
            'cloudinary_public_id': 'demo_aws_cert',
            'cloudinary_url': 'https://res.cloudinary.com/demo/image/upload/sample.jpg',
            'file_format': 'pdf',
            'verified_content_type': 'application/pdf',
            'file_size': 245000,
            'visibility': 'public'
        }
    )

    print("Demo data successfully seeded!")

if __name__ == '__main__':
    seed()
