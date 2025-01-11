from tkinter.font import names

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, UserCreateView, NotificationView, user_login

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('api/', include(router.urls)),
    path('registration/', UserCreateView.as_view()),
    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('login/', user_login, name='user_login'),
]
