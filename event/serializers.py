from rest_framework import serializers
from event.models import Event

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['creator', 'title', 'location', 'date', 'description', 'duration']

    def save(self):
        try:
            creator = self.validated_data['creator']
            title = self.validated_data['title']
            location = self.validated_data['location']
            description = self.validated_data['description']
            duration = self.validated_data['duration']
            
            event = Event(
                creator = creator,
                title = title,
                location = location,
                description = description,
                duration = duration,
            )

            event.save()
            return event
            
        except KeyError:
            raise serializers.ValidationError({"response": "You must have an event creator, title, location, description and duration"}) 