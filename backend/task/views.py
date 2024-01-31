from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import datetime
import logging


class TaskListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar y crear tareas.

    Permite a los usuarios listar todas las tareas existentes y crear 
    nuevas tareas proporcionando el contenido de la tarea.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['created_at', 'content']

    def perform_create(self, serializer):
        """
        Crea una nueva tarea y la asocia al usuario autenticado.
        """
        # Obtiene la instancia de la tarea antes de guardarla
        task_instance = serializer.save(user=self.request.user)
        
        # Actualiza los campos adicionales si están presentes en validated_data
        content = serializer.validated_data.get('content')
        completed = serializer.validated_data.get('completed')

        if content is not None:
            task_instance.content = content

        if completed is not None:
            task_instance.completed = completed
            if completed:
                task_instance.completed_at = datetime.datetime.now()

        task_instance.save()

        self.log_activity(f'Tarea creada: {task_instance}')

    def log_activity(self, message):
        """
        Log de la actividad del usuario.
        """
        logger = logging.getLogger(__name__)
        logger.info(message)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar y eliminar tareas.

    Permite a los usuarios ver, actualizar y eliminar sus propias tareas.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        """
        Actualiza la tarea y, si se marca como completada, establece la 
        fecha de completado.
        """
        completed = serializer.validated_data.get('completed', False)

        if completed:
            serializer.validated_data['completed_at'] = datetime.datetime.now()
        else:
            serializer.validated_data['completed_at'] = None

        serializer.save(content=serializer.validated_data['content'])

        self.log_activity(f'Tarea actualizada: {serializer.instance}')

    def perform_destroy(self, instance):
        """
        Elimina la tarea.
        """
        if instance:
            self.log_activity(f'Tarea eliminada: {instance}')
        instance.delete()

    def log_activity(self, message):
        """
        Log de la actividad del usuario.
        """
        logger = logging.getLogger(__name__)
        logger.info(message)
