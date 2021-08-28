from rest_framework import serializers
from account.models import Account

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'profile_pic', 'is_org', 'bio']
        extra_kwargs = {
            'password': {'write_only': True},
        }    


    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            password=self.validated_data['password'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            profile_pic=self.validated_data['profile_pic'],
            is_org=self.validated_data['is_org'],
            bio=self.validated_data['bio'],
        )
        account.set_password(self.validated_data['password'])
        account.save()
        return account

class AccountProfileSerializer(serializers.ModelSerializer):
    subscriber_count = serializers.SerializerMethodField('get_subscriber_count')
    subscribing_count = serializers.SerializerMethodField('get_subscribing_count')
    
    def get_subscriber_count(self, account):
        queryset = account.to_account_id.all()
        return len(queryset)
    
    def get_subscribing_count(self, account):
        queryset = account.from_account_id.all()
        return len(queryset)
    
    class Meta:
        model = Account
        fields = ['pk', 'email', 'username', 'first_name', 'last_name', 'bio', 'profile_pic', 'is_org', 'subscriber_count', 'subscribing_count']
