from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User, Code


class CodeTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='test', first_name='test',
                                        last_name='test')
        self.client.force_authenticate(user=self.user)

        self.code = Code.objects.create()

    def test_create_code(self):
        """ Тестирование создания кода"""

        response = self.client.post(
            '/code/create/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete_code(self):
        """ Тестирование создания кода"""

        response = self.client.post(
            '/code/create/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        response = self.client.post(
            '/code/delete/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
