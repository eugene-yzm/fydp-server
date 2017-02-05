from django.shortcuts import render


#from django.contrib.auth.models import User
from rest_framework import viewsets
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import DataPoint, User
from serializers import DataPointSerializer
from serializers import UserSerializer
from rest_framework import generics
from django.core.validators import validate_email
from django import forms
import bcrypt


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
# # Create your views here.


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


@csrf_exempt
def data_list(request):
    """
    List all data_points, or create a new snippet.
    """
    if request.method == 'GET':
        data = DataPoint.objects.all()
        #username = request.GET.get('username', None)
        # if username is not None:
        #     data = data.filter(user=username)
        data = data.filter(user=request.user)
        serializer = DataPointSerializer(data, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data = data.filter(user=request.user)
        #username = request.POST.get('username', None)
        #if username is not None:
        serializer = DataPointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

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


def user_data(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        params = request.GET

        if email_is_valid(params.get('email')):
            if user_exists(params.get('email')):
                user = find_user(params.get('email'))
                if params.get('password') and check_auth(user, params.get('password')):
                    serializer = UserSerializer(user)
                    return JSONResponse(serializer.data)
                else:
                    return JSONResponse('Reason: Authentication Failed', status=403)
            else:
                return JSONResponse('Reason: User does not exist', status=400)
        else:
            return JSONResponse('Reason: Invalid Email', status=400)


def create_user(request):
    data = JSONParser().parse(request)
    serializer = DataPointSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data)
    return JSONResponse(serializer.errors, status=400)


def user_exists(email):
    """
    :type: string
    :rtype: boolean
    """
    user = User.objects.filter(email=email)
    return len(user) > 0


def find_user(email):
    """
    :type: string
    :rtype: User
    """
    return User.objects.filter(email=email)[0]


def check_auth(user, password):
    """
    :type: User, string
    :rtype: boolean
    """
    print password.encode('utf-8'), user.password.encode('utf-8'), bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
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
    :type: int, string
    :rtype: boolean
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())