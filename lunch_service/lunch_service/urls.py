from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from service_api.views import (
    RestaurantViewSet,
    MenuViewSet,
    EmployeeViewSet,
    VoteViewSet,
    DayResultsView,
)

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurant")
router.register(r"menus", MenuViewSet, basename="menu")
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"votes", VoteViewSet, basename="vote")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/results/", DayResultsView.as_view(), name="results"),
]
