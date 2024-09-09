from django.contrib.auth.models import User
from rest_framework import serializers

from service_api.models import Restaurant, Menu, Employee, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

        def create(self, validated_data):
            user = validated_data.get("user")
            if not User.objects.filter(username=user.username).exists():
                user.save()
            employee = Employee.objects.create(**validated_data)
            return employee


class VoteSerializer(serializers.ModelSerializer):
    employee = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vote
        fields = "__all__"
