import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from quotes.models import Quote, Source, Category


class SetVoteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Motivation')
        self.source = Source.objects.create(name='Test Source', category=self.category, user=self.user)
        self.quote = Quote.objects.create(text='Test Quote', source=self.source, user=self.user, weight=10)

    def test_set_vote_invalid_value(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:vote', kwargs={'pk': self.quote.id})
        response = self.client.post(url, {'value': ''})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'status': 'error', 'message': 'Не указано значение голоса'})

    def test_set_vote_invalid_format(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:vote', kwargs={'pk': self.quote.id})
        response = self.client.post(url, {'value': 'invalid'})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'status': 'error', 'message': 'Неверный формат голоса'})

    @patch('api.services.process_vote')
    def test_set_vote_success(self, mock_process_vote):
        mock_process_vote.return_value = ('success', self.quote, 'Спасибо за ваш голос!')
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:vote', kwargs={'pk': self.quote.id})
        response = self.client.post(url, {'value': 1})
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)

        self.assertIn('success', response_data)
        self.assertIn('message', response_data)
        self.assertIn('item_html', response_data)

        self.assertEqual(response_data['success'], 'True')
        self.assertEqual(response_data['message'], 'Голос учтён')


class ChangeWeightViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Motivation')
        self.source = Source.objects.create(name='Test Source', category=self.category, user=self.user)
        self.quote = Quote.objects.create(text='Test Quote', source=self.source, user=self.user, weight=10)

    def test_change_weight_success(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:change-weight')
        response = self.client.post(url, {'weight': 20, 'quote_id': self.quote.id})
        self.quote.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'success': True, 'message': 'Вес цитаты успешно изменен.'})
        self.assertEqual(self.quote.weight, 20)

    def test_change_weight_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:change-weight')
        response = self.client.post(url, {'weight': 'invalid', 'quote_id': self.quote.id})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'success': False,
                                                                      'message': 'Неверный формат веса.'})


class DeleteQuoteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Motivation')
        self.source = Source.objects.create(name='Test Source', category=self.category, user=self.user)
        self.quote = Quote.objects.create(text='Test Quote', source=self.source, user=self.user, weight=10)

    def test_delete_quote_success(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:delete-quote')
        response = self.client.post(url, {'quote_id': self.quote.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'success': True, 'message': 'Цитата успешно удалена.'})
        self.assertFalse(Quote.objects.filter(id=self.quote.id).exists())

    def test_delete_quote_not_found(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('api:delete-quote')
        response = self.client.post(url, {'quote_id': 99999})
        self.assertEqual(response.status_code, 404)
