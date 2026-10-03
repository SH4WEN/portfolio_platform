from django.test import TestCase, Client as HttpClient
from django.contrib.auth.models import User
from django.urls import reverse
from apps.clients.models import Client
from apps.portfolios.models import Project, Skill, Experience, Education

class PortfolioPublicViewTest(TestCase):
    def setUp(self):
        self.http_client = HttpClient()
        self.staff_user = User.objects.create_user('admin', 'admin@example.com', 'password123', is_staff=True)
        
        self.published_client = Client.objects.create(
            name="Alice Cooper",
            email="alice@example.com",
            profession="Full-Stack Dev",
            headline="Web Developer",
            bio="Passionate builder",
            is_published=True
        )
        
        self.draft_client = Client.objects.create(
            name="Bob Builder",
            email="bob@example.com",
            profession="Draft Dev",
            headline="Work in progress",
            bio="Under construction",
            is_published=False
        )

        self.project = Project.objects.create(
            client=self.published_client,
            title="E-Commerce Engine",
            description="Scalable storefront system",
            tech_stack="Python, Django, PostgreSQL",
            is_published=True
        )

    def test_public_access_to_published_portfolio(self):
        response = self.http_client.get(reverse('portfolios:public_portfolio', kwargs={'slug': 'alice-cooper'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Cooper")
        self.assertContains(response, "E-Commerce Engine")

    def test_anonymous_access_to_unpublished_portfolio_returns_404(self):
        response = self.http_client.get(reverse('portfolios:public_portfolio', kwargs={'slug': 'bob-builder'}))
        self.assertEqual(response.status_code, 404)

    def test_staff_preview_access_to_unpublished_portfolio(self):
        self.http_client.login(username='admin', password='password123')
        response = self.http_client.get(reverse('portfolios:public_portfolio', kwargs={'slug': 'bob-builder'}) + '?preview=true')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bob Builder")
        self.assertContains(response, "STAFF PREVIEW MODE")

    def test_project_slug_uniqueness_per_client(self):
        proj1 = Project.objects.create(
            client=self.published_client,
            title="SaaS Platform",
            description="Multi-tenant app"
        )
        proj2 = Project.objects.create(
            client=self.published_client,
            title="SaaS Platform",
            description="Another version"
        )
        self.assertEqual(proj1.slug, "saas-platform")
        self.assertEqual(proj2.slug, "saas-platform-1")
