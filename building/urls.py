from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter

from building import views

router = SimpleRouter()
router.register('', views.BuildingViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
