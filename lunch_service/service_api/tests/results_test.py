import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from service_api.models import Vote, Menu, Restaurant, Employee


@pytest.mark.django_db
def test_result_for_users():
    user = User.objects.create_user(username="testuser1", password="12345678den")
    restaurant = Restaurant.objects.create(name="test restaurant")
    menu = Menu.objects.create(
        restaurant=restaurant, items="1, 2, 3", date="2024-09-09"
    )
    employee = Employee.objects.create(user=user, is_restaurant_worker=False)
    vote = Vote.objects.create(employee=employee, menu=menu, date="2024-09-09")

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/v1/results/", HTTP_X_APP_VERSION="2.0")

    assert response.data["menu_name"] == menu.items
    assert response.data["restaurant_name"] == restaurant.name
    assert response.data["vote_count"] == 1


@pytest.mark.django_db
def test_result_for_restaurant_workers():
    user = User.objects.create_user(username="testuser1", password="12345678den")
    restaurant = Restaurant.objects.create(name="test restaurant")
    menu = Menu.objects.create(
        restaurant=restaurant, items="1, 2, 3", date="2024-09-09"
    )
    employee = Employee.objects.create(user=user, is_restaurant_worker=True)
    vote = Vote.objects.create(employee=employee, menu=menu, date="2024-09-09")

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/v1/results/", HTTP_X_APP_VERSION="2.0")
    assert response.status_code == 403
