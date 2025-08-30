from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from quotes.models import Category, Source, Quote


class AddQuoteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(name='Motivation')
        self.source = Source.objects.create(name='Test Source', category=self.category, user=self.user)

    def test_add_quote_view_status_code(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('quotes:add-quote')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_quote_view_context(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('quotes:add-quote')
        response = self.client.get(url)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Добавить цитату')

    def test_add_valid_quote(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('quotes:add-quote')
        data = {
            'text': 'This is a test quote',
            'source': self.source.id,
            'weight': 10,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('quotes:index'))
        self.assertEqual(Quote.objects.count(), 1)

    def test_add_invalid_quote(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('quotes:add-quote')
        data = {
            'text': '',
            'source': self.source.id,
            'weight': 10,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('text', form.errors)
        self.assertIn('This field is required.', form.errors['text'])


class PopularQuotesViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(name='Motivation')
        self.source = Source.objects.create(name='Test Source', category=self.category, user=self.user)
        Quote.objects.create(text='Quote 1', source=self.source, user=self.user, weight=5)
        Quote.objects.create(text='Quote 2', source=self.source, user=self.user, weight=3)

    def test_popular_quotes_view_status_code(self):
        url = reverse('quotes:popular-quotes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_popular_quotes_view_context(self):
        url = reverse('quotes:popular-quotes')
        response = self.client.get(url)
        self.assertIn('quotes', response.context)
        self.assertEqual(len(response.context['quotes']), 2)
        self.assertEqual(response.context['title'], 'Популярные цитаты')

    def test_popular_quotes_view_queryset(self):
        url = reverse('quotes:popular-quotes')
        response = self.client.get(url)

        quotes = response.context['quotes']
        self.assertEqual(quotes[0].text, 'Quote 1')
        self.assertEqual(quotes[1].text, 'Quote 2')


class RandomQuoteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(name='Motivation')
        self.source = Source.objects.create(name='Test Source', category=self.category, user=self.user)
        self.quote = Quote.objects.create(text='Random Quote', source=self.source, user=self.user, weight=10)

    def test_random_quote_view_status_code(self):
        url = reverse('quotes:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_random_quote_view_context(self):
        url = reverse('quotes:index')
        response = self.client.get(url)
        self.assertIn('quote', response.context)
        self.assertEqual(response.context['quote'].text, 'Random Quote')
        self.assertEqual(response.context['title'], 'Случайная цитата')

    def test_random_quote_view_functionality(self):
        url = reverse('quotes:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
