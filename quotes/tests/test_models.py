from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from quotes.models import Quote, Source, Category, Vote

User = get_user_model()


class QuoteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass')
        self.cat = Category.objects.create(name='Книга')
        self.source = Source.objects.create(name='Source A', category=self.cat, user=self.user)

    def test_weight_validators(self):
        q = Quote(text='t', source=self.source, user=self.user, weight=0)
        with self.assertRaises(ValidationError):
            q.full_clean()

        q2 = Quote(text='t2', source=self.source, user=self.user, weight=101)
        with self.assertRaises(ValidationError):
            q2.full_clean()

        q3 = Quote(text='t3', source=self.source, user=self.user, weight=50)

        q3.full_clean()

    def test_save_enforces_three_quotes_limit(self):

        Quote.objects.create(text='q1', source=self.source, user=self.user, weight=1)
        Quote.objects.create(text='q2', source=self.source, user=self.user, weight=1)
        Quote.objects.create(text='q3', source=self.source, user=self.user, weight=1)

        q4 = Quote(text='q4', source=self.source, user=self.user, weight=1)
        with self.assertRaises(ValidationError):
            q4.save()

    def test_unique_text_source_raises_integrity_error(self):
        Quote.objects.create(text='same', source=self.source, user=self.user, weight=1)
        dup = Quote(text='same', source=self.source, user=self.user, weight=1)
        with self.assertRaises(IntegrityError):
            dup.save()


class VoteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vuser', password='pass')
        self.cat = Category.objects.create(name='Фильм')
        self.source = Source.objects.create(name='Source V', category=self.cat, user=self.user)
        self.quote = Quote.objects.create(text='vote quote', source=self.source, user=self.user, weight=1)

    def test_unique_vote_per_user_quote(self):
        Vote.objects.create(value=Vote.LIKE, quote=self.quote, user=self.user)
        dup = Vote(value=Vote.LIKE, quote=self.quote, user=self.user)
        with self.assertRaises(IntegrityError):
            dup.save()

    def test_vote_value_choices_validation(self):
        bad = Vote(value=2, quote=self.quote, user=self.user)
        with self.assertRaises(ValidationError):
            bad.full_clean()


class QuerySetMethodsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='qsu', password='pass')
        self.cat = Category.objects.create(name='Категория1')
        self.source1 = Source.objects.create(name='S1', category=self.cat, user=self.user)
        self.source2 = Source.objects.create(name='S2', category=self.cat, user=self.user)

        self.q1 = Quote.objects.create(text='q1', source=self.source1, user=self.user, weight=1)
        self.q2 = Quote.objects.create(text='q2', source=self.source1, user=self.user, weight=5)

        self.q3 = Quote.objects.create(text='q3', source=self.source2, user=self.user, weight=2)

        Vote.objects.create(value=Vote.LIKE, quote=self.q1, user=self.user)

        self.other = User.objects.create_user(username='other', password='pass')
        Vote.objects.create(value=Vote.DISLIKE, quote=self.q1, user=self.other)
        Vote.objects.create(value=Vote.LIKE, quote=self.q2, user=self.other)
        Vote.objects.create(value=Vote.LIKE, quote=self.q2, user=self.user)

    def test_get_random_weighted_returns_none_for_empty_qs(self):
        empty = Quote.objects.none()
        self.assertIsNone(empty.get_random_weighted())

    def test_get_random_weighted_uses_weights_with_patch(self):
        with patch('random.choices', return_value=[self.q2]) as mocked:
            chosen = Quote.objects.filter(source=self.source1).get_random_weighted()
            self.assertEqual(chosen.pk, self.q2.pk)
            mocked.assert_called_once()

    def test_with_votes_annotation_counts_correctly(self):
        qs = Quote.objects.with_votes()
        q1_annot = qs.get(pk=self.q1.pk)
        q2_annot = qs.get(pk=self.q2.pk)
        q3_annot = qs.get(pk=self.q3.pk)

        self.assertEqual(int(q1_annot.likes), 1)
        self.assertEqual(int(q1_annot.dislikes), 1)

        self.assertEqual(int(q2_annot.likes), 2)
        self.assertEqual(int(q2_annot.dislikes), 0)

        self.assertEqual(int(q3_annot.likes), 0)
        self.assertEqual(int(q3_annot.dislikes), 0)


class SourceCategoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='scuser', password='pass')
        self.cat1 = Category.objects.create(name='Cat A')
        self.cat2 = Category.objects.create(name='Cat B')

        self.s1 = Source.objects.create(name='Source 1', category=self.cat1, user=self.user)
        self.s2 = Source.objects.create(name='Source 2', category=self.cat1, user=self.user)
        self.s3 = Source.objects.create(name='Source 3', category=self.cat2, user=self.user)

        Quote.objects.create(text='a', source=self.s1, user=self.user, weight=1)
        Quote.objects.create(text='b', source=self.s1, user=self.user, weight=1)
        Quote.objects.create(text='c', source=self.s2, user=self.user, weight=1)

    def test_source_with_quotes_count(self):
        s_qs = Source.objects.with_quotes_count()
        s1 = s_qs.get(pk=self.s1.pk)
        s2 = s_qs.get(pk=self.s2.pk)
        s3 = s_qs.get(pk=self.s3.pk)

        self.assertEqual(int(s1.quotes_count), 2)
        self.assertEqual(int(s2.quotes_count), 1)
        self.assertEqual(int(s3.quotes_count), 0)

    def test_category_with_counts(self):
        c_qs = Category.objects.with_quotes_count().with_sources_count()
        c1 = c_qs.get(pk=self.cat1.pk)
        c2 = c_qs.get(pk=self.cat2.pk)

        self.assertEqual(int(c1.sources_count), 2)
        self.assertEqual(int(c1.quotes_count), 3)

        self.assertEqual(int(c2.sources_count), 1)
        self.assertEqual(int(c2.quotes_count), 0)
