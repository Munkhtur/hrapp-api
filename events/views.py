from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Events
from .serializer import EventSerializer
from rest_framework import permissions
# Create your views here.


class EventsList(ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        print(self.request, '>>>>>>>>>>>>>>>>>>>>')
        serializer.save(owner=self.request.user)
        print('event crkjajs;l')

    def get_queryset(self):
        return Events.objects.filter(owner=self.request.user)

# class EventsList(RetrieveUpdateDestroyAPIView):
#     serializer_class = EventSerializer
#     permission_classes = permissions.IsAuthenticated


#     def get_queryset(self):
#         return Events.objects.filter(owner=self.request.user)
