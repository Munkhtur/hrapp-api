from rest_framework.serializers import ModelSerializer
from .models import Events


class EventSerializer(ModelSerializer):

    class Meta:
        model = Events

        fields = ['content', 'type', 'date']
