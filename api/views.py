from django.shortcuts import render
from django.conf import settings

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from users.models import Student, Interest, InterestStatus
from chatbot.models import Feedback, IndividualNotification, GroupNotification
from .serializers import *


class StudentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = StudentSerializer
    # filter_backends = 
    # permission_classes = 

    def get_queryset(self):
        return Student.objects.get(user=self.request.user)

    # Overriding default retrieve function as it expects a URL keyword argument or lookup field
    def retrieve(self, request):
        serializer = self.serializer_class(self.get_queryset())
        return Response(serializer.data, status=status.HTTP_200_OK)

class SettingsAPIView(generics.RetrieveUpdateAPIView):
    # queryset = Student.objects.all()
    serializer_class = SettingsSerializer

    def get_queryset(self):
        return Student.objects.get(user=self.request.user)

    def retrieve(self, request):
        serializer = self.serializer_class(self.get_queryset())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request):
        serializer = self.serializer_class(self.get_queryset(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        # if serializer.is_valid():
        #     serializer.save(raise_exception=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

class FeedbackAPIView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer

class IndividualNotificationAPIView(generics.RetrieveAPIView):
    serializer_class = IndividualNotificationSerializer

    def get_queryset(self):
        return IndividualNotification.objects.filter(student=self.request.user.student)

    def retrieve(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GroupNotificationAPIView(generics.RetrieveAPIView):
    serializer_class = GroupNotificationSerializer

    def get_queryset(self):
        student = self.request.user.student
        student_class = student.current_class

        qs = InterestStatus.objects.filter(student=student, status=True).values_list('interest', flat=True)
        active_interests = list(qs)

        return GroupNotification.objects.filter(nclass=student_class, interest__in=active_interests)

    def retrieve(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QueryApiView(APIView):
    """Responding to user queries"""

    serializer_class = QuerySerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Generate response to query"""
        
        serializer = QuerySerializer(data=request.data)
        user = self.request.user

        if serializer.is_valid():
            query = serializer.data.get('query')
            response = requests.post( settings.RASA_URL, json={ "sender": f"{self.request.user.username}","message" : f"{query}" })

            if response:
                json_response = response.json()

                for idx in range(len(json_response)):
                    del json_response[idx]['recipient_id']

                return Response({'response': json_response})
            else:
                return Response({'response': {'text':'Something seems to be wrong with our Assistant. :( Try again later maybe?'} })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)