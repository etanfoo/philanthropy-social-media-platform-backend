from rest_framework import serializers
from Subscription.models import Subscription

class SubscribingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['pk', 'from_account_id']

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['pk', 'to_account_id']

class AddSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['pk', 'from_account_id', 'to_account_id']
    
    def save(self):
        subscription = Subscription(
            from_account_id=self.validated_data['from_account_id'],
            to_account_id=self.validated_data['to_account_id']
        )
        print(subscription)
        subscription.save()
        return subscription
    