from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from Post.serializers import PostCreateSerializer, PostSerializer, PostUpdateSerializer
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from Post.models import Post
from django.db.models import Q
from account.serializers import AccountProfileSerializer
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
            #print("serialiser is valid")
            post = serializer.save()
            data['post_id'] = post.pk
            data['image_url'] = post.image_url
            #data['account_id'] = post.account_id.pk
            data['title'] = post.title
            data['description'] = post.description
            data['is_mission'] = post.is_mission
            if (post.is_shared is not None):
                data['is_shared'] = post.is_shared.pk
            else:
                data['is_shared'] = None
            data['time_created'] = post.time_created
            data['dollar_target'] = post.dollar_target
            data['current_dollar'] = post.current_dollar
            data['username'] = post.account_id.username
            # print("can return")
            print(data)
            return Response(data = data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_shared_post_view(request):

    if request.method == 'POST':
        data = request.data.copy()
        data['account_id'] = request.user.pk
        data['is_shared'] = data['original_post_id']
        serializer = PostCreateSerializer(data = data)
        original_post_id = data['original_post_id']
        data = {}
        if serializer.is_valid():
            #print("serialiser is valid")
            post = serializer.save()

            data['post_id'] = post.pk
            data['image_url'] = post.image_url
            data['title'] = post.title
            data['description'] = post.description
            data['is_shared'] = original_post_id
            data['time_created'] = post.time_created
            original_data = {}
            original_post = Post.objects.filter(pk = original_post_id)[0]
            original_data['image_url'] = original_post.image_url
            original_data['post_id'] = original_post.pk
            original_data['title'] = original_post.title
            original_data['description'] = original_post.description
            original_data['is_mission'] = original_post.is_mission

            # if (post.is_shared is not None):
            #     original_data['is_shared'] = original_post.is_shared.pk
            # else:
            #     original_data['is_shared'] = None
            original_data['time_created'] = original_post.time_created
            original_data['dollar_target'] = original_post.dollar_target
            original_data['current_dollar'] = original_post.current_dollar
            original_data['username'] = original_post.account_id.username

            data['original_post'] = original_data
            # print(data)
            # print("can return")
            return Response(data = data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([])
class PostListView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = Post.objects.all().filter(is_shared__isnull=True).order_by('-time_created')
        return queryset


@permission_classes([])
class ProfilePostsView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = self.request.GET.get('user_id')
        if user_id is not None:
            queryset = Post.objects.filter(Q(account_id=user_id) & Q(is_shared__isnull=True)).order_by('-time_created')
            print(queryset)
        else: 
            queryset = Post.objects.all().filter(is_shared__isnull=True).order_by('-time_created')

        return queryset


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_feed_view(request):
    user = request.user
    yeet = user.from_account_id.all()
    ret = [AccountProfileSerializer(y.to_account_id).data.account_id for y in yeet]
    return Response({'subscribing': ret})

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_post_view(request):
    post_id = request.GET.get('post_id')
    try:
        post = Post.objects.get(pk=post_id)
    except:
        return Response({'response': 'Post does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def change_post_view(request):
    try:
        post = Post.objects.get(pk = request.data['post_id'])
        print(post)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if post.account_id != user:
        return Response({'response':"You don't have permission to edit that."}) 
        
    if request.method == 'PUT':
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'UPDATE SUCCESS'
            data['title'] = post.title
            data['image_url'] = post.image_url
            data['description'] = post.description
            data['dollar_target'] = post.dollar_target
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)