from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from event.models import Event
from participant.models import Participant
from participant.serializers import ParticipantCreateSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_participant_view(request):
    data = {
        'user_id': request.user.pk,
        'event': request.data.get('event_id'),
    }
    print(data)
    serializer = ParticipantCreateSerializer(data=data)
    if serializer.is_valid():
        participant = serializer.save()
        print('successful participant save')
        data['response'] = 'Attend Event successful!'
        prev_participant_count = Event.objects.filter(pk=data['event']).values('participant_count')
        print(prev_participant_count[0]['participant_count'])
        Event.objects.filter(pk = data['event']).update(participant_count = prev_participant_count[0]['participant_count'] + 1)
        return Response(data = data)
    else:
        print('unsucessful participant save')
        # Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    