import datetime

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from service_api.models import Restaurant, Menu, Employee, Vote
from service_api.persmissions import IsAdminOrReadOnly
from service_api.serializers import RestaurantSerializer, MenuSerializer, EmployeeSerializer, VoteSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly]


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(date=datetime.date.today())


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    #permission_classes = [IsAuthenticated]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        menu_id = request.data.get('menu')
        today = datetime.date.today()

        try:
            menu = Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            return Response({'detail': 'Invalid menu or menu not available for today.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if Vote.objects.filter(employee=user, date=today).exists():
            return Response({'detail': 'You have already voted today.'}, status=status.HTTP_400_BAD_REQUEST)

        vote = Vote(employee=user, menu=menu, date=today)
        vote.save()
        serializer = self.get_serializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

