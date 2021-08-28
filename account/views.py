from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView
from django.contrib.auth import authenticate, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from account.serializers import RegistrationSerializer, AccountProfileSerializer
from account.models import Account
from rest_framework.authtoken.models import Token
from account.validators import valid_email, valid_username

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    data = {}
    email = request.data.get('email', '0').lower()
    if valid_email(email) != None:
        data['error_message'] = 'Email is already in use!'
        data['response'] = 'ERROR'
        return Response(data)

    username = request.data.get('username', '0')
    if valid_username(username) != None:
        data['error_message'] = 'That username is already in use.'
        data['response'] = 'ERROR'
        return Response(data)

    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = 'Registration successful!'
    else:
        Response(data, status=status.HTTP_400_BAD_REQUEST)
    return Response(data)

# LOGIN
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        res = {}
        username = request.data.get('username')
        password = request.data.get('password')
        account = authenticate(username=username, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            res['response'] = 'Successful login!'
            res['user_id'] = account.pk
            res['username'] = account.username
            res['email'] = account.email
            res['first_name'] = account.first_name
            res['last_name'] = account.first_name
            res['bio'] = account.bio
            res['profile_pic'] = account.profile_pic
            res['is_org'] = account.is_org
            res['token'] = token.key
        else:
            res['response'] = 'ERROR'
            res['error_message'] = 'Invalid username/password'
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

        return Response(res)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_profile_view(request):
    print(request.user)
    user_id = request.GET.get('user_id')
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return Response({'response': 'Account does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AccountProfileSerializer(account)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def logout_view(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('Successfully Logged Out')


@permission_classes((IsAuthenticated,))
class ApiAccountListView(ListAPIView):
    serializer_class = AccountProfileSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('username')
    
    def get_queryset(self):
        query = self.request.GET.get('username')
        if query is not None:
            queryset = Account.objects.filter(
                Q(username__icontains=query)
                ).order_by('date_joined')
            print(queryset)
        else: 
            queryset = Account.objects.all().order_by('-date_joined')

        return queryset

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_subscriber_view(request):
    user = request.user
    yeet = user.to_account_id.all()
    ret = [AccountProfileSerializer(y.to_account_id).data for y in yeet]
    return Response({'subscribers': ret})


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_subscribing_view(request):
    user = request.user
    yeet = user.from_account_id.all()
    ret = [AccountProfileSerializer(y.from_account_id).data for y in yeet]
    return Response({'subscribing': ret})