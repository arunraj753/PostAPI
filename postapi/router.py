from rest_framework import routers
from postapi.viewsets import TagViewSet,PostViewSet,HomeViewSet

router = routers.DefaultRouter()
router.register('tag',TagViewSet)
router.register('post',PostViewSet,basename='post')
router.register('home',HomeViewSet,basename='home')