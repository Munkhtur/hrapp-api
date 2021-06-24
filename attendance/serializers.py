
from rest_framework.serializers import ModelSerializer
from .models import Attendance


class AttendanceSerializer(ModelSerializer):

    class Meta:
        model = Attendance

        fields = ['id', 'name', 'email', 'department', 'clockin', 'clockout',
                  'workhours', 'breakhours', 'status']


class AttentanceUpdateSerializer(ModelSerializer):

    class Meta:
        model = Attendance
        fields = ['clockin', 'clockout', 'workhours', 'breakhours', 'status']

    def update(self, instance, validated_data):
        instance.clockin = validated_data.get('clockin', instance.clockin)
        instance.clockout = validated_data.get('clockout', instance.clockout)
        instance.workhours = validated_data.get(
            'workhours', instance.workhours)
        instance.breakhours = validated_data.get(
            'breakhours', instance.breakhours)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
