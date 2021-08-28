from rest_framework import serializers
from participant.models import Participant

class ParticipantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['user_id', 'event']

    def save(self):
        try:
            user_id = self.validated_data['user_id']
            event = self.validated_data['event']

            participant = Participant(
                user_id = user_id,
                event = event
            )

            participant.save()
            return participant
            
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a participant and an event"}) 
