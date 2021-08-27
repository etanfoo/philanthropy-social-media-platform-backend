from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from Post.serializers import PostCreateSerializer
from rest_framework.response import Response


# Create your views here.
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_post_view(request):

    if request.method == 'POST':
        data = request.data.copy()
        data['account_id'] = request.user.pk
        serializer = PostCreateSerializer(data = data)

        data = {}
        if serializer.is_valid():
            print("serialiser is valid")
            post = serializer.save()
            data['post_id'] = post.pk
            data['image_url'] = post.image_url
            #data['account_id'] = post.account_id.pk
            data['title'] = post.title
            data['description'] = post.description
            data['is_mission'] = post.is_mission
            data['time_created'] = post.time_created
            data['dollar_target'] = post.dollar_target
            data['current_dollar'] = post.current_dollar
            data['username'] = post.account_id.username
            print("can return")
            print(data)
            return Response(data = data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
