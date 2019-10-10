import json
from io import BytesIO
from PIL import Image

from django.test import TestCase
from django.core.files.base import File
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.encoding import force_str

from venelin.gallery.models import Gallery, Picture


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


class GalleryApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_gallery = Gallery.objects.create(
            title='Active Gallery',
            slug='active-gallery',
        )
        Gallery.objects.create(
            title='Empty Gallery',
            slug='empty-gallery',
        )
        test_gallery.pictures.create(
            image=File(generate_image(), 'test-picture.png'),
            is_album_logo=True,
        )

    @classmethod
    def tearDownClass(cls):
        for picture in Picture.objects.all():
            default_storage.delete(picture.image.path)
            default_storage.delete(picture.thumb.path)

    def assertStartsWith(self, text, prefix, msg=None):
        if msg is None:
            msg = "'{text}' does not starts with '{prefix}'".format(text=text, prefix=prefix)
        self.assertTrue(text.startswith(prefix), msg)

    def test_ajax_list_galleries(self):
        response = self.client.get(reverse('gallery:index.json'))
        self.assertEqual(response.status_code, 200)
        actual = response.json()
        actual_cover = actual.get('data', [{}])[0].get('cover')
        expected = {
            'data': [
                {
                    'title': 'Active Gallery',
                    'slug': 'active-gallery',
                    'cover': actual_cover,
                },
            ]
        }
        self.assertEqual(actual, expected)
        self.assertStartsWith(actual_cover, '/media/CACHE/images/gallery/active-gallery/test-picture/')

    def test_ajax_get_active_gallery(self):
        response = self.client.get(reverse('gallery:gallery.json', args=['active-gallery']))
        self.assertEqual(response.status_code, 200)
        actual = response.json()
        actual_thumb = actual.get('data', {}).get('pictures', [{}])[0].get('thumb')
        expected = {
            'data': {
                'title': 'Active Gallery',
                'slug': 'active-gallery',
                'pictures': [
                    {
                        'title': 'test-picture.png',
                        'image': '/media/gallery/active-gallery/test-picture.jpg',
                        'thumb': actual_thumb,
                    },
                ],
            },
        }
        self.assertEqual(actual, expected)
        self.assertStartsWith(actual_thumb, '/media/CACHE/images/gallery/active-gallery/test-picture/')

    def test_ajax_get_empty_gallery(self):
        response = self.client.get(reverse('gallery:gallery.json', args=['empty-gallery']))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'errors': [{
                'code': 'NOT FOUND',
                'description': 'No Gallery matches the given query.'
            }],
        })
