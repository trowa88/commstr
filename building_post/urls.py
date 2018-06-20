from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter

from building_post import views

router = SimpleRouter()
router.register('', views.BuildingPostViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
