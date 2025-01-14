from tkinter.font import names

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, UserCreateView, NotificationView, user_login, RequestViewSet, req_create, req_list, \
    req_update, req_list_user, user_list

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'requests', RequestViewSet, basename='requests')
urlpatterns = [
    path('api/', include(router.urls)),
    path('registration/', UserCreateView.as_view()),
    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('login/', user_login, name='user_login'),
    path('req_create/', req_create, name='req_create'),
    path('req_list/', req_list, name='req_list'),
    path('req_update/', req_update, name='req_update'),
    path('req_list_user/<username>', req_list_user, name='req_list_user'),
    path('user_list/', user_list, name='user_list'),

]
