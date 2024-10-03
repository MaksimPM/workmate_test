from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from exhibition.models import Breed, Kitten
from django.contrib.auth import get_user_model

User = get_user_model()


class BreedViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpassword'
        )
        self.breed = Breed.objects.create(name='Siamese')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def authenticate(self):
        """Вспомогательная функция для аутентификации через JWT."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_list_breeds(self):
        """Тест вывода списка пород"""
        self.authenticate()
        url = reverse('exhibition:breed-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Siamese')


class KittenViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpassword'
        )
        self.breed = Breed.objects.create(name='Siamese')
        self.kitten = Kitten.objects.create(name='Fluffy', breed=self.breed, user=self.user, age=5, color='white')
        self.url = reverse('exhibition:kitten-list')  # URL для списка котят
        self.kitten_detail_url = reverse('exhibition:kitten-detail', kwargs={'pk': self.kitten.pk})

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def authenticate(self):
        """Вспомогательная функция для аутентификации через JWT."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_list_kittens_without_authentication(self):
        """Тест вывода списка котят без аутентификации"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_kittens_with_authentication(self):
        """Тест вывода списка котят с аутентификацией"""
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_kitten(self):
        """Тест создания  котят"""
        self.authenticate()
        data = {
            'name': 'Snowball',
            'breed': self.breed.pk,
            'age': 5,
            'description': 'Good kitten!',
            'color': 'white'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Snowball')

    def test_update_kitten(self):
        """Тест обновления информации о котятах"""
        self.authenticate()
        data = {'name': 'Fluffy Updated', 'breed': self.breed.pk, 'age': self.kitten.age, 'color': self.kitten.color}
        response = self.client.put(self.kitten_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.kitten.refresh_from_db()
        self.assertEqual(self.kitten.name, 'Fluffy Updated')

    def test_delete_kitten(self):
        self.authenticate()
        response = self.client.delete(self.kitten_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RatingViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpassword'
        )
        self.kitten = Kitten.objects.create(name='Fluffy', age=5, breed=Breed.objects.create(name='Siamese'),
                                            user=self.user, color='white')
        self.rating_url = reverse('exhibition:rating-list')

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def authenticate(self):
        """Вспомогательная функция для аутентификации через JWT."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_rating_without_authentication(self):
        """Тест оценки котят без аутентификации"""
        data = {
            'kitten': self.kitten.pk,
            'rating': 5
        }
        response = self.client.post(self.rating_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_rating_with_authentication(self):
        """Тест оценки котят с аутентификацией"""
        self.authenticate()
        data = {
            'kitten': self.kitten.pk,
            'rating': 5
        }
        response = self.client.post(self.rating_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)
