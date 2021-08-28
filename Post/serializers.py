from rest_framework import serializers
from Post.models import Post

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_account')
    profile_pic = serializers.SerializerMethodField('get_profile_pic_from_account')

    def get_username_from_account(self, post):
        username = post.account_id.username
        return username

    def get_profile_pic_from_account(self, post):
        pfp = post.account_id.profile_pic
        return pfp

    class Meta:
        model = Post
        fields = ['pk', 'image_url', 'username', 'profile_pic', 'account_id', 'title', 'description', 'is_mission', 'is_shared', 'time_created', 'dollar_target', 'current_dollar']

class PostUpdateSerializer(serializers.ModelSerializer):
     class Meta:
        model = Post
        fields = ['title', 'image_url', 'description', 'dollar_target']   

     def validate(self, post):
        try:
            title = post['title']
            image_url = post['image_url']
            description = post['description']
            dollar_target = post['dollar_target']
        except KeyError:
            pass
        return post 

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