from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from quotes.models import Quote, Source, Category


class DashBoardQuotesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Motivation')
        self.source = Source.objects.create(name='Test Source', category=self.category, user=self.user)
        self.quote = Quote.objects.create(text='Test Quote', source=self.source, user=self.user, weight=10)
        self.quote2 = Quote.objects.create(text='Another Test Quote', source=self.source, user=self.user, weight=5)

    def test_dashboard_quotes_view_status_code(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('dashboard:quotes', kwargs={'category_id': self.category.id, 'source_id': self.source.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_quotes_view_context(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('dashboard:quotes', kwargs={'category_id': self.category.id, 'source_id': self.source.id})
        response = self.client.get(url)
        self.assertIn('quotes', response.context)
        self.assertEqual(len(response.context['quotes']), 2)
        self.assertEqual(response.context['title'], 'Дашборд Цитат')
        self.assertEqual(response.context['source'], self.source)

    def test_dashboard_quotes_view_queryset(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('dashboard:quotes', kwargs={'category_id': self.category.id, 'source_id': self.source.id})
        response = self.client.get(url)
        quotes = response.context['quotes']
        self.assertEqual(quotes[0].text, 'Test Quote')
        self.assertEqual(quotes[1].text, 'Another Test Quote')


class DashBoardSourcesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Motivation')
        self.source1 = Source.objects.create(name='Source 1', category=self.category, user=self.user)
        self.source2 = Source.objects.create(name='Source 2', category=self.category, user=self.user)

    def test_dashboard_sources_view_status_code(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('dashboard:sources', kwargs={'category_id': self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_sources_view_context(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('dashboard:sources', kwargs={'category_id': self.category.id})
        response = self.client.get(url)
        self.assertIn('sources', response.context)
        self.assertEqual(len(response.context['sources']), 2)
        self.assertEqual(response.context['title'], 'Дашборд Источников')
        self.assertEqual(response.context['category'], self.category)

    def test_dashboard_sources_view_queryset(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('dashboard:sources', kwargs={'category_id': self.category.id})
        response = self.client.get(url)
        sources = response.context['sources']
        self.assertEqual(sources[0].name, 'Source 1')
        self.assertEqual(sources[1].name, 'Source 2')


class DashBoardCategoriesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category1 = Category.objects.create(name='Motivation')
        self.category2 = Category.objects.create(name='Inspiration')

    def test_dashboard_categories_view_status_code(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('dashboard:categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_categories_view_context(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('dashboard:categories')
        response = self.client.get(url)
        self.assertIn('categories', response.context)
        self.assertEqual(len(response.context['categories']), 2)
        self.assertEqual(response.context['title'], 'Дашборд категорий')

    def test_dashboard_categories_view_queryset(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('dashboard:categories')
        response = self.client.get(url)
        categories = response.context['categories']
        self.assertEqual(categories[0].name, 'Motivation')
        self.assertEqual(categories[1].name, 'Inspiration')
