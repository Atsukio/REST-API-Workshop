from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from core.users.api.views import ToDoViewSet, UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("todos", ToDoViewSet)


app_name = "api"
urlpatterns = router.urls
