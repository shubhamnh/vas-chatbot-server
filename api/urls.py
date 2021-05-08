from django.urls import path, include
from .views import StudentDetailAPIView, SettingsAPIView, FeedbackAPIView, IndividualNotificationAPIView, GroupNotificationAPIView, QueryApiView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Authentication
    path('token-auth/', TokenObtainPairView.as_view(), name='token_auth'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    # User Info
    path('profile/', StudentDetailAPIView.as_view(), name='profile'),
    path('settings/', SettingsAPIView.as_view(), name='settings'),
    path('feedback/', FeedbackAPIView.as_view(), name='feedback'),
    path('individualnotif/', IndividualNotificationAPIView.as_view(), name='individual_notif'),
    path('groupnotif/', GroupNotificationAPIView.as_view(), name='group_notif'),
    path('query/', QueryApiView.as_view(), name='query'),
]