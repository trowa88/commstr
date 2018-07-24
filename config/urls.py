from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_nested import routers

from building.views import BuildingViewSet
from building_post.views import BuildingPostViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  url(r"^$", TemplateView.as_view(template_name="pages/home.html"), name="home"),
                  url(
                      r"^about/$",
                      TemplateView.as_view(template_name="pages/about.html"),
                      name="about",
                  ),
                  # Django Admin, use {% url 'admin:index' %}
                  url(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  url(
                      r"^users/",
                      include("jwt_drf.users.urls", namespace="users"),
                  ),
                  url(r"^accounts/", include("allauth.urls")),
                  # Your stuff: custom urls includes go here
                  # jwt auth
                  url(r'^api-token-auth/', obtain_jwt_token),
                  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
                  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
              ] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(
            r"^400/$",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        url(
            r"^403/$",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        url(
            r"^404/$",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        url(r"^500/$", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns

router = routers.SimpleRouter()
router.register(r'buildings', BuildingViewSet)

building_router = routers.NestedSimpleRouter(router, r'buildings', lookup='building')
building_router.register(r'posts', BuildingPostViewSet, base_name='building-posts')

urlpatterns += [
    path('api/', include(router.urls)),
    path('api/', include(building_router.urls)),
]
