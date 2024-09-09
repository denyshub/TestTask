import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from service_api.models import Vote, Menu, Restaurant, Employee


@pytest.mark.django_db
def test_vote_creation():
    user = User.objects.create_user(username="testuser1", password="12345678den")
    restaurant = Restaurant.objects.create(name="test restaurant")
    menu = Menu.objects.create(
        restaurant=restaurant, items="1, 2, 3", date="2024-09-09"
    )
    employee = Employee.objects.create(user=user, is_restaurant_worker=False)
    vote = Vote.objects.create(employee=employee, menu=menu, date="2024-09-09")
    assert vote.employee == employee
    assert vote.menu == menu
    assert vote.date.strftime("%Y-%m-%d") == "2024-09-09"
    assert Vote.objects.count() == 1


@pytest.mark.django_db
def test_vote_creation_by_restaurant_employee():
    user = User.objects.create_user(username="testuser1", password="12345678den")
    restaurant = Restaurant.objects.create(name="test restaurant")
    menu = Menu.objects.create(
        restaurant=restaurant, items="1, 2, 3", date="2024-09-09"
    )
    employee = Employee.objects.create(user=user, is_restaurant_worker=True)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/v1/votes/", {"menu": menu.id, "date": "2024-09-09"}, format="json"
    )

    assert response.status_code == 403
