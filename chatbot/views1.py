from django.shortcuts import render
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets, status, filters, mixins
from . import serializers, models, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from push_notifications.models import WebPushDevice
# from rasa_nlu.training_data import load_data
# from rasa_nlu.config import RasaNLUModelConfig
# from rasa_nlu.model import Trainer
# from rasa_nlu.model import Metadata, Interpreter
# from rasa_core.interpreter import RasaNLUInterpreter
# import re
# from actions import Actions
# from datetime import datetime
# from database_conf import Database


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    permission_classes = (permissions.UpdateOwnProfile, IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'rollno'
    search_fields = ('name', 'rollno')

class UserInfoViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Getting info of logged in user"""

    serializer_class = serializers.UserInfoSerializer
    permission_classes = (permissions.UpdateOwnProfile, IsAuthenticated,)
    lookup_field = 'rollno'
    queryset = models.UserProfile.objects.all()

class QueryApiView(APIView):
    """Responding to user queries"""

    serializer_class = serializers.QuerySerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.UserProfile.objects.all()
    string_list = ['Hi', 'Hey', 'Hello', 'Sup']

    def post(self, request):
        """Generate response to query"""

        serializer = serializers.QuerySerializer(data=request.data)
        user = self.request.user
        if serializer.is_valid():
            query = serializer.data.get('query')
            resp = 'Is your name {0}?<br/>And roll no. {1}??'.format(user.name, user.rollno)

            for string in self.string_list:
                if string.lower() in query.lower():
                    resp = 'Hey! <br/>How you doin? ;)'

            return Response({'response': resp})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotifApiView(APIView):
    """Responding to Group Notification Requests"""

    serializer_class = serializers.NotifSerializer
    permission_classes = (IsAuthenticated,)
    queryset = (models.UserProfile.objects.all(), models.GroupNotification.objects.all())

    def get(self, request):
        """Get Notifications as per user Class & Interests"""

        user = self.request.user
        class_column = ''

        if (user.ayear == 'SE'):
            class_column = 'se_cmpn_'
        elif (user.ayear == 'TE'):
            class_column = 'te_cmpn_'
        else:
            class_column = 'be_cmpn_'

        if (user.division == 'A'):
            class_column = class_column + 'a'
        elif (user.division == 'B'):
            class_column = class_column + 'b'
        else:
            class_column = class_column + 'c'

        user_interests = ''
        if (user.workshop):
            user_interests += ' | Q(interest=\'workshop\')'
        if (user.sports):
            user_interests += ' | Q(interest=\'sports\')'
        if (user.creative):
            user_interests += ' | Q(interest=\'creative\')'
        if (user.cultural):
            user_interests += ' | Q(interest=\'cultural\')'
        if (user.placement):
            user_interests += ' | Q(interest=\'placement\')'
        if (user.dance):
            user_interests += ' | Q(interest=\'dance\')'
        if (user.drama):
            user_interests += ' | Q(interest=\'drama\')'
        if (user.study):
            user_interests += ' | Q(interest=\'study\')'

        if (len(user_interests)>0):
            user_interests = user_interests[3:]

        kwargs = {
            '{0}'.format(class_column,): 'True',
        }
        args = (eval(user_interests),)

        notifs = models.GroupNotification.objects.all().filter(*args, **kwargs).order_by('-nid')
        serializer = serializers.NotifSerializer(notifs, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Post Notif"""

        serializer = serializers.NotifSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IndividualNotifApiView(APIView):
    """Responding to personal notif request"""

    serializer_class = serializers.IndividualNotifSerializer
    # permission_classes = (permissions.AllowPost,)
    permission_classes = (IsAuthenticated,)
    queryset = (models.UserProfile.objects.all(), models.Individual.objects.all())

    def get(self, request):
        """Get Individual Notifications"""

        user = self.request.user
        notifs = models.Individual.objects.all().filter(rollno=user.rollno).order_by('-id')
        serializer = serializers.IndividualNotifSerializer(notifs, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Post Individual Push Notification"""
    
        serializer = serializers.IndividualNotifSerializer(data=request.data)
        if serializer.is_valid():
            device = WebPushDevice.objects.filter(name=request.data.get('rollno'))
            if device.exists():
                device.send_message(request.data.get('notice'))
            else:
                print ('No subscribed user with this roll no')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupportApiView(APIView):
    """Support/Feedback"""

    serializer_class = serializers.SupportSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'rollno'
    queryset = (models.UserProfile.objects.all())

    def post(self, request):
        """Post Feedback"""

        user = self.request.user
        serializer = serializers.SupportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(name=user.name, rollno=user.rollno)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Change user password"""

    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.UpdateOwnProfile, IsAuthenticated,)
    lookup_field = 'rollno'
    queryset = models.UserProfile.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance.password = make_password(serializer.validated_data.get('passw'))
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response('Successfully changed!', status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        serializer.save()
