from rest_framework import serializers
from authentication.api.serializers import UserSerializer
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'content', 'created_at', 'completed', 'completed_at']

        def validate_content(self, value):
            if len(value) < 10:
                raise serializers.ValidationError("El contenido debe tener al menos 10 caracteres.")
            return value
    
    def validate(self, data):
        user = self.context['request'].user
        completed = data.get('completed', False)
        completed_at = data.get('completed_at', None)

        # Verificar si ya existe una tarea completada para el mismo usuario en la misma fecha y hora
        if completed and completed_at:
            existing_completed_task = Task.objects.filter(
                user=user,
                completed=True,
                completed_at=completed_at
            ).exclude(id=data.get('id', None)).exists()

            if existing_completed_task:
                raise serializers.ValidationError("Ya existe una tarea completada en esta fecha y hora.")

        return data
