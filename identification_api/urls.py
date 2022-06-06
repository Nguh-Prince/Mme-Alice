from django.urls import path
from rest_framework_extensions.routers import NestedRouterMixin

from rest_framework import routers

from . import views

class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass

router = NestedDefaultRouter()

people_routes = router.register("api/people", views.PersonViewSet, basename="people")
people_routes.register(
    "ids", views.IdentifictionViewSet, basename="person-ids", parents_query_lookups=["person"]
)

identification_routes = router.register("api/ids", views.IdentifictionViewSet, basename='ids')
identification_routes

urlpatterns = router.urls