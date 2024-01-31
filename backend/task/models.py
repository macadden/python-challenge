from django.db import models
from authentication.models import User

class Task(models.Model):
    """
    Modelo para representar una tarea.

    Cada tarea tiene un usuario asociado, contenido, fecha de creación, 
    estado de completado y fecha de completado (si está completada).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """
        Devuelve una representación de cadena de la tarea.
        """
        return f'{self.user.username} - {self.created_at}'
