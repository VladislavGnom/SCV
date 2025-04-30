from django.test import SimpleTestCase
from django.urls import reverse, resolve
from quiz.views import test_view, test_result_view, TestStatisticsView


class TestUrls(SimpleTestCase):

    def test_test_view_is_resolves(self):
        url = reverse('test-main', args=['1'])
        self.assertEqual(resolve(url).func, test_view)

    def test_test_result_view_is_resolves(self):
        url = reverse('test-result', args=['1'])
        self.assertEqual(resolve(url).func, test_result_view)

    def test_test_statistics_view_is_resolves(self):
        url = reverse('test-statistics')
        self.assertEqual(resolve(url).func.view_class, TestStatisticsView)

    def test_handle_test_view_is_resolves(self):
        url = reverse('submit-test', args=['1'])
        self.assertEqual(resolve(url).func, test_view)
        