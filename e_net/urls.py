from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from e_net.views import NetworkNodeViewSet

router = DefaultRouter()
router.register(r"network-nodes", NetworkNodeViewSet, basename="networknode")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls), include("e_net.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
