from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from venelin.blog.models import Entry, Category


class BlogTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(title='Linux', slug='linux')
        cls.category2 = Category.objects.create(title='Django', slug='django')
        cls.category3 = Category.objects.create(title='No public entries', slug='no-public-entries')
        cls.category4 = Category.objects.create(title='No entries', slug='no-entries')

        cls.category1entry1 = Entry.objects.create(
            title="Post About Linux",
            slug='post-about-linux',
            category=cls.category1,
            content="<p>Content about Linux</p>",
            is_published=True,
            created=timezone.now() - timedelta(days=10)
        )

        cls.category1entry2 = Entry.objects.create(
            title="Unpublished Post About Linux",
            slug='unpublished-post-about-linux',
            category=cls.category1,
            content="<p>Content about Linux</p>",
            is_published=False,
            created=timezone.now() - timedelta(days=6)
        )

        cls.category2entry1 = Entry.objects.create(
            title="Post About Django",
            slug='post-about-django',
            category=cls.category2,
            content="<p>Content about Django</p>",
            is_published=True,
            created=timezone.now() - timedelta(days=4)
        )

        cls.category2entry2 = Entry.objects.create(
            title="Second Post About Django",
            slug='second-post-about-django',
            category=cls.category2,
            content="<p>Content about Django</p>",
            is_published=True,
        )

        cls.category3entry = Entry.objects.create(
            title="Unpublished Post",
            slug='unpublished-post',
            category=cls.category3,
            content="<p>Unpublished content</p>",
            is_published=False,
            created=timezone.now() - timedelta(days=2)
        )

    def test_number_of_published_entries(self):
        self.assertEqual(Entry.objects.published().count(), 3)

    def test_number_of_active_categories(self):
        self.assertEqual(list(Category.objects.active().values()), [
            {
                'id': 2,
                'title': 'Django',
                'slug': 'django',
                'entries_count': 2,
            },
            {
                'id': 1,
                'title': 'Linux',
                'slug': 'linux',
                'entries_count': 1,
            },
        ])

    def test_blog_index_view(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

    def test_blog_category_index_view(self):
        response = self.client.get(self.category1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_blog_category_index_view_empty(self):
        response = self.client.get(self.category3.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.category4.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_blog_entry_view(self):
        response = self.client.get(self.category1entry1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_blog_entry_view_unpublished(self):
        response = self.client.get(self.category1entry2.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_blog_feed(self):
        response = self.client.get(reverse('blog:feed'))
        self.assertEqual(response.status_code, 200)
