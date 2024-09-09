from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from service_api.models import Restaurant, Menu, Employee, Vote
from service_api.persmissions import IsAdminOrReadOnly, IsRestaurantEmployeeOrReadOnly

from service_api.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    EmployeeSerializer,
    VoteSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly]


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    permission_classes = [IsRestaurantEmployeeOrReadOnly]

    def get_queryset(self):
        today = timezone.now().date()
        return Menu.objects.filter(date=today)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        if user.is_anonymous:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            employee = Employee.objects.get(user=user)
            if employee.is_restaurant_worker:
                return Response(
                    {"detail": "Restaurant employees cannot vote."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND
            )

        menu_id = request.data.get("menu")
        today = timezone.now().date()

        try:
            menu = Menu.objects.get(id=menu_id, date=today)
        except Menu.DoesNotExist:
            return Response(
                {"detail": "Invalid menu."}, status=status.HTTP_400_BAD_REQUEST
            )

        if Vote.objects.filter(employee=employee, date=today).exists():
            return Response(
                {"detail": "You have already voted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        vote = Vote(employee=employee, menu=menu, date=today)
        vote.save()

        serializer = self.get_serializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DayResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        user = request.user

        if hasattr(user, "employee") and user.employee.is_restaurant_worker:
            return Response(
                {"detail": "Restaurant employees cannot access voting results."},
                status=status.HTTP_403_FORBIDDEN,
            )

        today = timezone.now().date()

        most_voted_menu = (
            Vote.objects.filter(date=today)
            .values("menu")
            .annotate(vote_count=Count("id"))
            .order_by("-vote_count")
            .first()
        )

        if not most_voted_menu:
            return Response(
                {"detail": "No votes found for today."},
                status=status.HTTP_404_NOT_FOUND,
            )

        menu_id = most_voted_menu["menu"]
        menu = Menu.objects.get(id=menu_id)
        restaurant = menu.restaurant

        return Response(
            {
                "menu_name": menu.items,
                "restaurant_name": restaurant.name,
                "vote_count": most_voted_menu["vote_count"],
            },
            status=status.HTTP_200_OK,
        )
