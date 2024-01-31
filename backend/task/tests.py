from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from authentication.models import User
from .models import Task

class TaskTests(TestCase):
    def setUp(self):
        # Crea un usuario para las pruebas
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            name='Test',
            last_name='User'
        )
        # Crea una tarea asociada al usuario
        self.task = Task.objects.create(
            user=self.user,
            content='Test Task'
        )
        # Configura un cliente API para realizar solicitudes HTTP
        self.client = APIClient()
        # Inicia sesión como el usuario de prueba
        self.client.force_authenticate(user=self.user)

    def test_task_list_create_view(self):
        url = reverse('tasks-list-create')
        data = {'content': 'New Task'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verifica que la tarea fue creada correctamente
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().content, 'New Task')

    def test_task_detail_view(self):
        url = reverse('tasks-detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica que los detalles de la tarea sean correctos
        self.assertEqual(response.data['content'], 'Test Task')

    def test_task_update_view(self):
        url = reverse('tasks-detail', args=[self.task.id])
        data = {'content': 'Updated Task'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica que la tarea fue actualizada correctamente
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, 'Updated Task')

    def test_task_delete_view(self):
        url = reverse('tasks-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
