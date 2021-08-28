from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from Subscription.serializers import AddSubscriptionSerializer
from Subscription.models import Subscription

# Create your views here.
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def subscribe_view(request):
    data = {
        'from_account_id': request.user.pk,
        'to_account_id': request.data.get('to_account_id'),
    }
    print(data)
    serializer = AddSubscriptionSerializer(data=data)
    if serializer.is_valid():
        account = serializer.save()
        print('yeet')
        data['response'] = 'Follow successful!'
    else:
        print('bleet')
        Response(data, status=status.HTTP_400_BAD_REQUEST)
    return Response(data)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def unsubscribe_view(request):
    res = {}
    try:
        subscription = Subscription.objects.get(from_account_id=request.user.pk, to_account_id=request.data.get('to_account_id'))
    except:
        res['response'] = 'Subscription does not exist'
        return Response(res, status=status.HTTP_404_NOT_FOUND)
    
    deletion = subscription.delete()
    res = {}
    if deletion:
        res['response'] = 'Unsubscription Successful!'
        return Response(res)
    res['response'] = 'Unsubscription failed!'
    return Response(res, status=status.HTTP_400_BAD_REQUEST)