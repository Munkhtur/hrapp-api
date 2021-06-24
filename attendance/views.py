from django.shortcuts import render
from django.shortcuts import (get_object_or_404)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, UpdateAPIView
from .models import Attendance
from .serializers import AttendanceSerializer, AttentanceUpdateSerializer
from rest_framework import permissions, request, status
from rest_framework.response import Response

# Create your views here.


class AttendanceList(ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Attendance.objects.all()


class AttendanceDetail(RetrieveAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        print(pk)
        return Attendance.objects.filter(pk=pk)


class AttendanceUpdate(UpdateAPIView):
    serializer_class = AttentanceUpdateSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, id):
        # id = self.kwargs['id']
        print(id)
        print(request.data, '>>>>>>>>>>>>>>>>>>')
        toUpdate = Attendance.objects.get(id=id)
        print(toUpdate, "toupdate>L>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        serializer = AttentanceUpdateSerializer(
            instance=toUpdate, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
