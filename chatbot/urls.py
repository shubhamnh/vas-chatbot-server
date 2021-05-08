from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from push_notifications.api.rest_framework import WebPushDeviceAuthorizedViewSet
from .views import QueryApiView, NotifApiView, IndividualNotifApiView, UserProfileViewSet, UserInfoViewSet, ChangePasswordViewSet

router = DefaultRouter()
router.register('profile', UserProfileViewSet)
router.register('info', UserInfoViewSet, basename='chatbot')
# router.register('changepass', views.ChangePasswordViewSet, basename='chatbot')
router.register(r'device/wpd', WebPushDeviceAuthorizedViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^query/', QueryApiView.as_view()),
    url(r'^notifs/', NotifApiView.as_view()),
    url(r'^personal/', IndividualNotifApiView.as_view()),
    url(r'^support/', SupportApiView.as_view()),
]
