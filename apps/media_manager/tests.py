import io
from PIL import Image
from django.test import TestCase, Client as HttpClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from apps.clients.models import Client
from apps.media_manager.models import PortfolioFile
from apps.media_manager.validators import validate_file_upload

class MediaManagerValidationTest(TestCase):
    def test_valid_image_upload_validation(self):
        # Create valid dummy PNG image in memory
        img_bytes = io.BytesIO()
        img = Image.new('RGB', (100, 100), color='cyan')
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        uploaded_file = SimpleUploadedFile("avatar.png", img_bytes.read(), content_type="image/png")
        result = validate_file_upload(uploaded_file)
        self.assertEqual(result['verified_content_type'], 'image/png')
        self.assertEqual(result['resource_type'], 'image')

    def test_invalid_file_extension_rejection(self):
        uploaded_file = SimpleUploadedFile("malicious.exe", b"binary content", content_type="application/octet-stream")
        with self.assertRaises(ValidationError):
            validate_file_upload(uploaded_file)

    def test_valid_pdf_signature_validation(self):
        pdf_content = b"%PDF-1.4 header and sample PDF body content"
        uploaded_file = SimpleUploadedFile("resume.pdf", pdf_content, content_type="application/pdf")
        result = validate_file_upload(uploaded_file)
        self.assertEqual(result['verified_content_type'], 'application/pdf')
        self.assertEqual(result['resource_type'], 'raw')


class MediaManagerSecurityTest(TestCase):
    def setUp(self):
        self.http_client = HttpClient()
        self.staff_user = User.objects.create_user('admin', 'admin@example.com', 'password123', is_staff=True)
        self.client_obj = Client.objects.create(
            name="Media Client",
            email="media@example.com",
            profession="Designer",
            headline="Creative director",
            bio="Visual expert",
            is_published=True
        )

        self.public_file = PortfolioFile.objects.create(
            client=self.client_obj,
            display_title="Public Portfolio Image",
            original_filename="image.jpg",
            category="certificate",
            cloudinary_public_id="portfolios/test/123",
            cloudinary_url="https://res.cloudinary.com/demo/image/upload/sample.jpg",
            file_format="jpg",
            verified_content_type="image/jpeg",
            file_size=1024,
            visibility="public"
        )

        self.private_file = PortfolioFile.objects.create(
            client=self.client_obj,
            display_title="Private Executive Resume",
            original_filename="resume_private.pdf",
            category="resume",
            cloudinary_public_id="portfolios/test/456",
            cloudinary_url="https://res.cloudinary.com/demo/raw/authenticated/resume.pdf",
            file_format="pdf",
            verified_content_type="application/pdf",
            file_size=2048,
            visibility="private"
        )

    def test_public_file_appears_on_public_portfolio(self):
        response = self.http_client.get(reverse('portfolios:public_portfolio', kwargs={'slug': 'media-client'}))
        self.assertContains(response, "Public Portfolio Image")
        self.assertNotContains(response, "Private Executive Resume")

    def test_anonymous_cannot_download_private_file(self):
        response = self.http_client.get(reverse('media_manager:private_download', kwargs={'pk': self.private_file.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/login/', response.url)

    def test_staff_user_can_download_private_file(self):
        self.http_client.login(username='admin', password='password123')
        response = self.http_client.get(reverse('media_manager:private_download', kwargs={'pk': self.private_file.pk}))
        self.assertEqual(response.status_code, 302)
