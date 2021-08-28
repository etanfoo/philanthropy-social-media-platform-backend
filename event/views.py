from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from event.models import Event
from event.serializers import EventCreateSerializer

# Create your views here.
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_event_view(request):

    if request.method == 'POST':
        data = request.data.copy()
        data['creator'] = request.user.pk
        serializer = EventCreateSerializer(data = data)
        
        fields = ['creator', 'title', 'location', 'date', 'description', 'duration']

        data = {}
        if serializer.is_valid():
            #print("serialiser is valid")
            event = serializer.save()
            data['event_id'] = event.pk
            data['creator'] = event.creator.pk
            data['title'] = event.title
            data['location'] = event.location
            data['date'] = event.date
            data['description'] = event.description
            data['duration'] = event.duration
            data['creator_username'] = event.creator.username

            print("can return")
            print(data)
            return Response(data = data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)