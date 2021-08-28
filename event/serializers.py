from rest_framework import serializers
from event.models import Event

class EventSerializer(serializers.ModelSerializer):
    creator_username = serializers.SerializerMethodField('get_username_from_account')
    profile_pic = serializers.SerializerMethodField('get_profile_pic_from_account')

    def get_username_from_account(self, event):
        creator_username = event.creator.username
        return creator_username

    def get_profile_pic_from_account(self, event):
        pfp = event.creator.profile_pic
        return pfp

    class Meta:
        model = Event
        fields = ['pk', 'creator', 'creator_username', 'profile_pic', 'title', 'location', 'date', 'description', 'duration', 'event_pic', 'participant_count']


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['creator', 'title', 'location', 'date', 'description', 'duration', 'event_pic']

    def save(self):
        try:
            creator = self.validated_data['creator']
            title = self.validated_data['title']
            location = self.validated_data['location']
            description = self.validated_data['description']
            duration = self.validated_data['duration']
            event_pic = self.validated_data['event_pic']
            date = self.validated_data['date']

            event = Event(
                creator = creator,
                title = title,
                location = location,
                description = description,
                duration = duration,
                event_pic = event_pic,
                date = date
            )

            event.save()
            return event
            
        except KeyError:
            raise serializers.ValidationError({"response": "You must have an event creator, title, location, description and duration"}) 


class EventUpdateSerializer(serializers.ModelSerializer):
     class Meta:
        model = Event
        fields = ['title', 'location', 'date', 'description', 'duration', 'event_pic', 'participant_count']   

     def validate(self, event):
        try:
            title = event['title']
            location = event['location']
            date = event['date']
            description = event['description']
            duration = event['duration']
            event_pic = event['event_pic']
            participant_count = event['participant_count']
        except KeyError:
            pass
        return event 