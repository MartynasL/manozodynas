# encoding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Translation, Word
from manozodynas.testutils import StatefulTesting


class IndexTestCase(StatefulTesting):
    def test_index_page(self):
        self.open(reverse('index'))
        self.assertStatusCode(200)


class LoginTestCase(StatefulTesting):

    fixtures = ['test_fixture.json']

    def test_login_page(self):
        self.open(reverse('login'))
        self.assertStatusCode(200)

    def test_good_login(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'test',
            'password': 'test',
        })
        self.assertStatusCode(302)

    def test_bad_login(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'bad',
            'password': 'bad',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')

    def test_no_input(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': '',
            'password': '',
        })
        self.assertStatusCode(200)
        self.selectMany('.errorlist')

    def test_no_username(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': '',
            'password': 'test',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')

    def test_no_password(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'test',
            'password': '',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')


class TranslationListTestCase(StatefulTesting):
    fixtures = ['translationlist_test_fixture.json']

    def test_vote_plus(self):
        self.open(reverse('translation_list'))
        self.selectForm('#vote_form_1')
        self.submitForm({'plus': '+', })
        self.assertStatusCode(200)
        self.assertEqual(Translation.objects.get(pk=1).vote, 1)

    def test_vote_minus(self):
        self.open(reverse('translation_list'))
        self.selectForm('#vote_form_1')
        self.submitForm({'minus': '-', })
        self.assertStatusCode(200)
        self.assertEqual(Translation.objects.get(pk=1).vote, -1)


class AddWordTest(StatefulTesting):
    fixtures = ['translationlist_test_fixture.json']

    def test_add_existing_word(self):
        self.open('add_word')
        self.selectForm('#add_word_form')
        self.submitForm({'value': 'hello', })
        self.assertStatusCode(200)
        self.assertEqual(Word.objects.filter(value='hello').count(), 1)

    def test_add_new_word(self):
        self.open('add_word')
        self.selectForm('#add_word_form')
        self.submitForm({'value': 'goodbye', })
        self.assertStatusCode(302)
        self.assertNotEqual(Word.objects.get(value='goodbye'), None)