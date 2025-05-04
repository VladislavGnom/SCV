from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from quiz.models import Test, UserTestResult

User = get_user_model()

class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        self.test = Test.objects.create(
            title='Sample Test',
            results_visibility=Test.VisibilityChoices.ALL,
        )

    def test_user_test_view_no_login(self):
        url_query = reverse('test-main', args=['1'])
        response = self.client.get(url_query)
        self.assertEqual(response.status_code, 302)

    def test_user_test_view_login(self):
        UserTestResult.objects.create(user=self.user, test=self.test)

        self.client.login(username='testuser', password='12345')
        url_query = reverse('test-main', args=[self.test.pk])
        response = self.client.get(url_query)
        self.assertEqual(response.status_code, 200)

    def test_handle_test_view_no_login(self):
        url_query = reverse('submit-test', args=['1'])
        response = self.client.post(url_query)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login', response.url)

    def test_handle_test_view_login(self):
        UserTestResult.objects.create(user=self.user, test=self.test)

        self.client.login(username='testuser', password='12345')
        url_query = reverse('submit-test', args=[self.test.pk])
        response = self.client.post(url_query)
        self.assertEqual(response.status_code, 302)

    def test_test_statistics_view_no_login(self):
        url_query = reverse('test-statistics')
        response = self.client.get(url_query)
        self.assertEqual(response.status_code, 302)
    
    def test_test_statistics_view_login(self):
        self.client.login(username='testuser', password='12345')
        url_query = reverse('test-statistics')
        response = self.client.get(url_query)
        self.assertEqual(response.status_code, 200)

    def test_test_result_view_no_login(self):
        url_query = reverse('test-result', args=[self.test.pk])
        response = self.client.get(url_query)
        self.assertEqual(response.status_code, 302)

    def test_test_result_view_login(self):
        user_test = UserTestResult.objects.create(user=self.user, test=self.test, is_passed=True)

        # ALL VISIBILITY STATUS && IS_PASSED = TRUE
        self.client.login(username='testuser', password='12345')
        url_query = reverse('test-result', args=[self.test.pk])
        response = self.client.get(url_query)
        self.assertEqual(response.status_code, 200)

        # HIDDEN VISIBILITY STATUS && IS_PASSED = TRUE
        self.test.results_visibility = self.test.VisibilityChoices.HIDDEN
        self.test.save()

        response = self.client.get(url_query)
        self.assertEqual(response.status_code, 302)

        # ALL VISIBILITY STATUS && IS_PASSED = FALSE
        user_test.is_passed = False
        self.test.results_visibility = self.test.VisibilityChoices.ALL
        self.test.save()
        user_test.save()

        response = self.client.get(url_query)
        self.assertEqual(response.status_code, 302)

        # HIDDEN VISIBILITY STATUS && IS_PASSED = FALSE
        user_test.is_passed = False
        self.test.results_visibility = self.test.VisibilityChoices.HIDDEN
        self.test.save()

        response = self.client.get(url_query)
        self.assertEqual(response.status_code, 302)

    def test_test_view_test_is_passed_correct_behaviour(self):
        UserTestResult.objects.create(user=self.user, test=self.test, is_passed=True)

        self.client.login(username='testuser', password='12345')
        url_query = reverse('test-main', args=[self.test.pk])
        response = self.client.get(url_query)

        self.assertEqual(response.status_code, 302)
