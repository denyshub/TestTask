import pytest
from django.db import IntegrityError

from service_api.models import Menu, Restaurant


@pytest.mark.django_db
def test_menu_creation():
    restaurant = Restaurant.objects.create(name="test restaurant")
    menu = Menu.objects.create(
        restaurant=restaurant, items="1, 2, 3", date="2024-09-09"
    )
    assert menu.restaurant == restaurant
    assert menu.items == "1, 2, 3"
    assert menu.date == "2024-09-09"
    assert Menu.objects.count() == 1


@pytest.mark.django_db
def test_menu_creation_unique_constraint():
    restaurant = Restaurant.objects.create(name="test restaurant")

    Menu.objects.create(restaurant=restaurant, items="1, 2, 3", date="2024-09-09")

    with pytest.raises(IntegrityError):
        Menu.objects.create(restaurant=restaurant, items="1, 2, 3", date="2024-09-09")
