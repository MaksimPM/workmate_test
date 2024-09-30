from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BreedViewSet, KittenViewSet, RatingViewSet
from exhibition.apps import ExhibitionConfig

app_name = ExhibitionConfig.name

router = DefaultRouter()
router.register(r'breeds', BreedViewSet)
router.register(r'kittens', KittenViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('exhibition/', include(router.urls)),
]

