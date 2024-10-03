from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        """Тест успешной регистрации пользователя"""
        response = self.client.post('/users/sign-up/', {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_registration_missing_fields(self):
        """Тест регистрации пользователя с недостающими полями"""
        response = self.client.post('/users/sign-up/', {
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_authentication(self):
        """Тест успешной аутентификации пользователя"""
        self.test_user_registration()
        response = self.client.post('/users/sign-in/', {
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_authentication_failure(self):
        """Тест неудачной аутентификации пользователя (неверный пароль)"""
        User.objects.create(email='test@example.com', password='testpassword')
        response = self.client.post('/users/sign-in/', {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_authentication_missing_credentials(self):
        """Тест аутентификации пользователя без указания email и пароля"""
        response = self.client.post('/users/sign-in/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmailConfirmationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='testuser',
            email='test@example.com',
            password='testpassword123',
            confirmation_code='123456'
        )
        self.client.force_authenticate(user=self.user)

    def test_email_confirmation_success(self):
        """Тест успешного подтверждения email"""
        response = self.client.post('/users/confirm_email/', {
            'confirmation_code': '123456'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Email успешно подтверждён!')

        self.user.refresh_from_db()
        self.assertTrue(self.user.email_validated)
        self.assertIsNone(self.user.confirmation_code)

    def test_email_confirmation_invalid_code(self):
        """Тест неудачного подтверждения с неверным кодом"""
        response = self.client.post('/users/confirm_email/', {
            'confirmation_code': 'wrongcode'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Неверный код или код устарел.')

        self.user.refresh_from_db()
        self.assertFalse(self.user.email_validated)
