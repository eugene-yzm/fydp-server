#from django.contrib.auth.models import User
from rest_framework import serializers
from models import DataPoint, User


# class DataPointSerializer(serializers.ModelSerializer):
    # # id = serializers.IntegerField(read_only=True)
    # # tag = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # # time = serializers.DateTimeField() # time sensor generates values
    # # temperature = serializers.DecimalField()
    # # humidity = serializers.DecimalField()
    # # orientation = serializers.DecimalField()
    #


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ('id', 'created' ,'time', 'tag','temperature','humidity','orientation')

    def create(self, validated_data):
        """
        Create and return a new `DataPoint` instance, given the validated data.
        """
        return DataPoint(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `DataPoint` instance, given the validated data.
        """
        instance.title = validated_data.get('tag', instance.tag)
        instance.time = validated_data.get('time', instance.time)
        instance.temperature = validated_data.get('temperature', instance.temperature)
        instance.humidity = validated_data.get('humidity', instance.humidity)
        instance.orientation = validated_data.get('orientation', instance.orientation)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    datapoints = DataPointSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'datapoints')

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return User(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

