from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from push_notifications.api.rest_framework import WebPushDeviceAuthorizedViewSet
from . import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('info', views.UserInfoViewSet, basename='chatbot')
# router.register('changepass', views.ChangePasswordViewSet, basename='chatbot')
router.register(r'device/wpd', WebPushDeviceAuthorizedViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^query/', views.QueryApiView.as_view()),
    url(r'^notifs/', views.NotifApiView.as_view()),
    url(r'^personal/', views.IndividualNotifApiView.as_view()),
    url(r'^support/', views.SupportApiView.as_view()),
]
