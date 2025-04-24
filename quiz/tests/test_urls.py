from django.test import SimpleTestCase
from django.urls import reverse, resolve
from quiz.views import test_view


class TestUrls(SimpleTestCase):

    def test_test_view_is_resolves(self):
        url = reverse('test-main', args=['1'])
        self.assertEqual(resolve(url).func, test_view)
        