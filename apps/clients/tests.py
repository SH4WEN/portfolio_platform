from django.test import TestCase, Client as HttpClient
from django.contrib.auth.models import User
from django.urls import reverse
from apps.clients.models import Client

class ClientModelTest(TestCase):
    def setUp(self):
        self.client_1 = Client.objects.create(
            name="John Doe",
            email="john@example.com",
            profession="Full-Stack Engineer",
            headline="Building scalable platforms",
            bio="Experienced software architect",
            is_published=True
        )

    def test_unique_slug_generation(self):
        self.assertEqual(self.client_1.slug, "john-doe")
        
        # Create second client with duplicate name
        client_2 = Client.objects.create(
            name="John Doe",
            email="john2@example.com",
            profession="Backend Developer",
            headline="Python expert",
            bio="Software engineer"
        )
        self.assertEqual(client_2.slug, "john-doe-1")

    def test_client_str(self):
        self.assertEqual(str(self.client_1), "John Doe")


class ClientViewSecurityTest(TestCase):
    def setUp(self):
        self.http_client = HttpClient()
        self.staff_user = User.objects.create_user('admin', 'admin@example.com', 'password123', is_staff=True)
        self.normal_user = User.objects.create_user('user', 'user@example.com', 'password123')
        self.client_obj = Client.objects.create(
            name="Sherwin Sarmiento",
            email="sherwin@example.com",
            profession="Lead Architect",
            headline="Cloud & AI Engineer",
            bio="Architecting modern web solutions",
            is_published=True
        )

    def test_anonymous_cannot_access_client_dashboard(self):
        response = self.http_client.get(reverse('clients:client_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/login/', response.url)

    def test_staff_user_can_access_client_dashboard(self):
        self.http_client.login(username='admin', password='password123')
        response = self.http_client.get(reverse('clients:client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sherwin Sarmiento")

    def test_client_create_view(self):
        self.http_client.login(username='admin', password='password123')
        response = self.http_client.post(reverse('clients:client_create'), {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'profession': 'DevOps Specialist',
            'headline': 'Kubernetes & CI/CD',
            'bio': 'Cloud infrastructure lead',
            'is_published': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Client.objects.filter(name='Jane Smith').exists())
