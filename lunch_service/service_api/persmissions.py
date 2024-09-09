# core/permissions.py
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if (
            request.method in ["GET", "HEAD", "OPTIONS"]
            and request.user.is_authenticated
        ):
            return True
        return request.user and request.user.is_staff


class IsRestaurantEmployeeOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

            # Дозволяємо доступ до POST запитів для співробітників ресторану
        if request.method == "POST":
            return (
                hasattr(request.user, "employee")
                and request.user.employee.is_restaurant_worker
            )

            # Всі інші запити заборонені для співробітників ресторану
        if hasattr(request.user, "employee"):
            return False

        return True


class IsNotRestaurantEmployee(BasePermission):

    def has_permission(self, request, view):
        # Дозволити доступ тільки тим, хто не є працівником ресторану
        if request.user.is_authenticated:
            # Якщо користувач - працівник ресторану, то доступ заборонено
            if (
                hasattr(request.user, "employee")
                and request.user.employee.is_restaurant_worker
            ):
                return False
        return True
