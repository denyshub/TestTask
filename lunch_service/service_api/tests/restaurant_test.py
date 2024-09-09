import pytest
from service_api.models import Restaurant


@pytest.mark.django_db
def test_restaurant_creation():
    restaurant = Restaurant.objects.create(name="test restaurant")
    assert restaurant.name == "test restaurant"
    assert Restaurant.objects.count() == 1
