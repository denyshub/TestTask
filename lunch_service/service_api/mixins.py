from django.utils import timezone
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from service_api.models import Menu, Vote


class DayResultsMixin:
    def get_today_results(self, version):
        today = timezone.now().date()
        most_voted_menu = (
            Vote.objects.filter(date=today)
            .values("menu")
            .annotate(vote_count=Count("id"))
            .order_by("-vote_count")
            .first()
        )
        if not most_voted_menu:
            return self.get_error_response(
                "No votes found for today.", status.HTTP_404_NOT_FOUND
            )

        menu_id = most_voted_menu["menu"]
        menu = self.get_menu(menu_id)

        if not menu:
            return self.get_error_response("Menu not found.", status.HTTP_404_NOT_FOUND)

        return self.format_response(menu, most_voted_menu, version)

    def get_menu(self, menu_id):
        try:
            return Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            return None

    def get_error_response(self, detail, status_code):
        return Response({"detail": detail}, status=status_code)

    def format_response(self, menu, most_voted_menu, version):
        if version == "1.0":
            return Response(
                {
                    "menu_name": menu.items,
                    "vote_count": most_voted_menu["vote_count"],
                },
                status=status.HTTP_200_OK,
            )
        elif version == "2.0":
            restaurant = menu.restaurant
            return Response(
                {
                    "menu_name": menu.items,
                    "restaurant_name": restaurant.name,
                    "vote_count": most_voted_menu["vote_count"],
                },
                status=status.HTTP_200_OK,
            )
        else:
            return self.get_error_response(
                "Unsupported version", status.HTTP_400_BAD_REQUEST
            )
