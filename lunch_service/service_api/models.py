from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    date = models.DateField()
    items = models.TextField()

    class Meta:
        unique_together = ("restaurant", "date")

    def __str__(self):
        return str(self.items)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_restaurant_worker = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee}, {self.menu}"
