from rest_framework import serializers
from Donate.models import Donate

class DonateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donate
        fields = ['account_id_from', 'post_id_to', 'amount', 'is_recurring', 'start_date', 'occurence', 'times_donated']

    def save(self):
        try:
            account_id_from = self.validated_data['account_id_from']
            post_id_to = self.validated_data['post_id_to']
            amount = self.validated_data['amount']
            is_recurring = self.validated_data['is_recurring']
            
            if ('occurence' in self.validated_data):
                occurence = self.validated_data['occurence']
            else:
                occurence = None
            
        
            donate = Donate(
                account_id_from = account_id_from,
                post_id_to = post_id_to,
                amount = amount,
                is_recurring = is_recurring,
                occurence = occurence,
            )

            donate.save()
            return donate
            
        except KeyError:
            raise serializers.ValidationError({"response": "You must have an account_id_from, post_id_to, amount and is_recurring"}) 