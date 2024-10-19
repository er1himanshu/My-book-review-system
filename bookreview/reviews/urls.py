from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, ReviewViewSet, UserRegisterView, UserLoginView, HomeView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/', include(router.urls)),
    path('api/register/', UserRegisterView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='login'),
]
