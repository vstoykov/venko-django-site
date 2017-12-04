import json
from io import BytesIO
from PIL import Image

from django.test import TestCase
from django.core.files.base import File
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.encoding import force_str

from venelin.gallery.models import Gallery


def generate_image():
    logo = BytesIO()
    Image.new("RGBA", size=(212, 150), color=(256, 128, 64)).save(logo, 'png')
    logo.seek(0)
    return logo


class GalleryAdminTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_admin_pk = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        ).pk
        cls.gallery_pk = Gallery.objects.create(
            title='Test Gallery',
            slug='test-gallery',
        ).pk

    def setUp(self):
        self.user_admin = get_user_model().objects.get(pk=self.user_admin_pk)
        self.gallery = Gallery.objects.get(pk=self.gallery_pk)

    def tearDown(self):
        for picture in self.gallery.pictures.all():
            default_storage.delete(picture.image.path)
            default_storage.delete(picture.thumb.path)

    def test_ajax_upload(self):
        self.client.force_login(self.user_admin)
        response = self.client.post(
            reverse('admin:gallery_gallery_upload', args=[self.gallery.pk]),
            {
                'image': File(generate_image(), 'test-picture.png'),
            }
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, self.gallery.pictures.count())
        picture = self.gallery.pictures.get()
        self.assertEqual(json.loads(force_str(response.content)), {
            'picture': {
                'pk': picture.pk,
                'gallery': self.gallery.pk,
                'title': 'test-picture.png',
                'image': {
                    'url': picture.image.url,
                    'thumbnail': picture.thumb.url,
                }
            }
        })

    def test_ajax_bad_upload(self):
        self.client.force_login(self.user_admin)
        response = self.client.post(
            reverse('admin:gallery_gallery_upload', args=[self.gallery.pk]),
            {'bad': 'data'},
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, self.gallery.pictures.count())
        self.assertIn('errors', json.loads(force_str(response.content)))

    def test_ajax_upload_missing_gallery(self):
        self.client.force_login(self.user_admin)
        response = self.client.post(
            reverse('admin:gallery_gallery_upload', args=[404]),
            {
                'image': File(generate_image(), 'test-picture.png'),
            }
        )
        self.assertEqual(404, response.status_code)

    def test_ajax_upload_permission(self):
        user = get_user_model().objects.create_user(
            username='staff',
            email='staff@example.com',
            password='staff',
            is_staff=True,
            is_superuser=False,
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse('admin:gallery_gallery_upload', args=[self.gallery.pk]),
            {
                'image': File(generate_image(), 'test-picture.png'),
            }
        )
        self.assertEqual(403, response.status_code)
