from rest_framework import serializers
from Post.models import Post

#Not sure what to do with this atm
class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_account')

    class Meta:
        model = Post
        fields = ['image_url', 'username', 'account_id', 'title', 'description', 'is_mission', 'is_shared', 'time_created','dollar_target', 'current_dollar']

    def get_username_from_account(self, post):
        username = post.account_id.username
        return username


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['image_url', 'account_id', 'title', 'description', 'is_mission', 'is_shared', 'time_created', 'dollar_target', 'current_dollar']

    def save(self):
        try:
            image_url = self.validated_data['image_url']
            account_id = self.validated_data['account_id']
            title = self.validated_data['title']
            description = self.validated_data['description']
            is_mission = self.validated_data['is_mission']
            if ('is_shared' in self.validated_data):
                is_shared = self.validated_data['is_shared']
            else:
                is_shared = None
            if ('dollar_target' in self.validated_data):
                dollar_target = self.validated_data['dollar_target']
            else:
                dollar_target = None
            #current_dollar = self.validated_data['current_dollar']
            #time_created = self.validated_data['time_created']

            post = Post(
                image_url = image_url,
                account_id = account_id,
                title = title,
                description = description,
                is_mission = is_mission,
                is_shared = is_shared,
                dollar_target = dollar_target,
                
            )

            post.save()
            return post
            
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, description, and a a dollar target."}) 