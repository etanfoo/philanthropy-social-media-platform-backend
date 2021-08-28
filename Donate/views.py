from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from Donate.models import Donate
from Donate.serializers import DonateCreateSerializer, DonateUpdateSerializer
from Post.models import Post

# Create your views here.
# Create your views here.
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_donate_view(request):

    if request.method == 'POST':
        data = request.data.copy()
        data['account_id'] = request.user.pk
        serializer = DonateCreateSerializer(data = data)
        
        data = {}
        if serializer.is_valid():
            #print("serialiser is valid")
            donate = serializer.save()
            if (donate.post_id_to.is_mission != True):
                return Response({'response': 'Post is not a mission'}, status=status.HTTP_404_NOT_FOUND)
            else:
                data['donate_id'] = donate.pk
                data['account_id_from'] = donate.account_id_from.pk
                data['post_id_to'] = donate.post_id_to.pk
                data['amount'] = donate.amount
                data['is_recurring'] = donate.is_recurring
                if (donate.occurence is not None):
                    data['occurence'] = donate.occurence
                else:
                    data['occurence'] = None
                data['start_date'] = donate.start_date
                data['times_donated'] = donate.times_donated
                data['username'] = donate.account_id_from.username

                post = Post.objects.get(pk = data['post_id_to'])
                prev_current_dollar = post.current_dollar
                if (prev_current_dollar is None):
                    prev_current_dollar = 0
                Post.objects.filter(pk=data['post_id_to']).update(current_dollar = prev_current_dollar + data['amount'])
                print(prev_current_dollar)

                print("can return")
                print(data)
                return Response(data = data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def change_donate_view(request):
    try:
        donate = Donate.objects.get(pk = request.data['donate_id'])
        print(donate)
    except Donate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if donate.account_id_from != user:
        return Response({'response':"You don't have permission to edit that."}) 
        
    if request.method == 'PUT':
        serializer = DonateUpdateSerializer(donate, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'UPDATE SUCCESS'
            data['amount'] = donate.amount
            data['occurence'] = donate.occurence
            data['is_recurring'] = donate.is_recurring
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def delete_donate_view(request):
    try:
        donate = Donate.objects.get(pk = request.data['donate_id'])
    except Donate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if donate.account_id_from != user:
        return Response({'resonse': "You don't have permission to delete this post!"})

    if request.method == "DELETE":
        operation = donate.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)