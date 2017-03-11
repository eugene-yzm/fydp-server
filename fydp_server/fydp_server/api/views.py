from django.shortcuts import render


#from django.contrib.auth.models import User
from rest_framework import viewsets
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from models import DataPoint, User
from serializers import DataPointSerializer
from serializers import UserSerializer
from rest_framework import generics
from django.core.validators import validate_email
from django import forms
import bcrypt


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# Unused Functions
#
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# # class UserViewSet(viewsets.ModelViewSet):
# #     """
# #     API endpoint that allows users to be viewed or edited.
# #     """
# #     queryset = User.objects.all().order_by('-date_joined')
# #     serializer_class = UserSerializer
# # # Create your views here.
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# @csrf_exempt
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer


@csrf_exempt
def data_list(request):
    """
    List all data_points, or create a new snippet.
    """
    if request.method == 'GET':
        params = request.GET
        response = authenticate(params)
        if response is None:
            user = find_user('access_data_key', params['access_data_key'])
            data = DataPoint.objects.filter(user=user)
            print data
            serializer = DataPointSerializer(data, many=True)
            return JSONResponse(serializer.data)
        else:
            return response
        # data = JSONParser().parse(request)
        # data = data.filter(user=request.user)
        # #username = request.POST.get('username', None)
        # #if username is not None:
        # serializer = DataPointSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JSONResponse(serializer.data, status=201)
        # return JSONResponse(serializer.errors, status=400)

    elif request.method == 'POST':
        params = request.GET
        data = JSONParser().parse(request)
        response = authenticate(params)
        if response is None:
            user = find_user('access_data_key', params.get('access_data_key'))
            if user is not None:
                data['user'] = user.id
                print data
                serializer = DataPointSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JSONResponse(serializer.data, status=201)
                return JSONResponse(serializer.errors, status=400)
        else:
            return response


@csrf_exempt
def data_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        datapoint = DataPoint.objects.get(pk=pk)
    except DataPoint.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DataPointSerializer(datapoint)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DataPointSerializer(datapoint, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    # elif request.method == 'DELETE':
    #     datapoint.delete()
    #     return HttpResponse(status=204)


@csrf_exempt
def user_data(request):
    """
    :type: HttpRequest
    :rtype: JSONResponse
    """
    if request.method == 'GET':
        params = request.GET
        response = authenticate(params)
        if response is None:
            user = find_user('email', params.get('email'))
            serializer = UserSerializer(user)
            return JSONResponse(serializer.data)
        else:
            return response
    return JSONResponse({'Reason': 'Something went wrong'}, status=400)

@csrf_exempt
def create_user(request):
    """
    :type: HttpRequest
    :rtype: JSONResponse
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        if all([k in data for k in ['password', 'email', 'name']]):
            data['password'] = hash_password(data['password'])
            data['access_data_key'] = hash_password(data['password'])
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            return JSONResponse(serializer.errors, status=400)
        else:
            return JSONResponse({'Reason': 'Missing Information or Invalid Input'}, status=400)
    return JSONResponse({'Reason': 'Something went wrong'}, status=400)


def authenticate(params):
    if 'email' in params:
        if email_is_valid(params.get('email')):
            if user_exists(params.get('email')):
                user = find_user('email', params.get('email'))
                if params.get('password') and check_auth(user, params.get('password')):
                    return None
                else:
                    return JSONResponse({'Reason': 'Authentication Failed'}, status=403)
            else:
                return JSONResponse({'Reason': 'User does not exist'}, status=400)
        else:
            return JSONResponse({'Reason': 'Invalid Email'}, status=400)
    if 'access_data_key' in params:
        if access_key_exists(params.get('access_data_key')):
            user = find_user('access_data_key', params.get('access_data_key'))
            if user is not None:
                return None
        else:
            return JSONResponse({'Reason': 'Invalid Access Key'}, status=400)
    return JSONResponse({'Reason': 'Invalid Params'}, status=400 )


def access_key_exists(key):
    user = User.objects.filter(access_data_key=key)
    return len(user) > 0


def user_exists(email):
    """
    :type: string
    :rtype: boolean
    """
    user = User.objects.filter(email=email)
    return len(user) > 0


def find_user(by_type, val):
    """
    :type: string, string
    :rtype: User
    """
    if by_type == 'email':
        return User.objects.filter(email=val)[0]
    if by_type == 'access_data_key':
        users = User.objects.filter(access_data_key=val)
        if len(users) > 0:
            return users[0]
        return None



def check_auth(user, password):
    """
    :type: User, string
    :rtype: boolean
    """
    #print password.encode('utf-8'), user.password.encode('utf-8'), bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    return bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))


def email_is_valid(email):
    """
    :type: string
    :rtype: boolean
    """
    try:
        validate_email(email)
        return True
    except forms.ValidationError:
        return False


def hash_password(password):
    """
    :type: string
    :rtype: boolean
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
