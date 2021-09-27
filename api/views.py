from django.conf import settings

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from datetime import datetime
from json2html import *

from users.models import Student, Interest, InterestStatus
from chatbot.models import Feedback, IndividualNotification, GroupNotification
from .serializers import *


class StudentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.get(user=self.request.user)

    # Overriding default retrieve function as it expects a URL keyword argument or lookup field
    def retrieve(self, request):
        serializer = self.serializer_class(self.get_queryset())
        return Response(serializer.data, status=status.HTTP_200_OK)

class SettingsAPIView(generics.RetrieveUpdateAPIView):
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

    def post(self, request):
        """Generate response to query"""
        serializer = QuerySerializer(data=request.data)

        if serializer.is_valid():
            query = serializer.data.get('query')
            response = requests.post(settings.RASA_URL, json = {
                "sender": f"{self.request.user.username}",
                "message": f"{query}"
            })

            if response:
                json_response = response.json()

                print(json_response)

                for idx in range(len(json_response)):
                    del json_response[idx]['recipient_id']

                    if 'custom' in json_response[idx]:
                        custom = json_response[idx]['custom']
                        intent = custom['intent']
                        
                        if intent == 'timetable':
                            return timetable_response(self)
                        elif intent == 'timetable_day':
                            return timetable_day_response(self, custom['day'])
                        else:
                            return Response(create_text_response('My maker has made some stupid decisions. Sorry for the trouble. :('))

                return Response({'response': json_response})
            else:
                return Response(create_text_response('Something seems to be wrong with our Assistant. :( Try again maybe?'))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def timetable_response(self):
    student = self.request.user.student
    student_class = student.current_class
    qs = TimeTable.objects.filter(tclass=student_class).order_by('weekday')

    serializer = TimetableSerializer(qs, many=True)

    text = 'Your timetable for the week is as follows:'
    table = json2html.convert(json = serializer.data)
    response = create_response([{'text':text},{'table':table}])

    return Response(response, status=status.HTTP_200_OK)
    
def timetable_day_response(self, day):
    student = self.request.user.student
    student_class = student.current_class
    today = datetime.now().weekday()

    qs = TimeTable.objects.filter(tclass=student_class)
    day = day.lower()

    if day == 'today':
        qs = qs.filter(weekday=today)
    elif day == 'tomorrow':
        qs = qs.filter(weekday=today+1)
    else:
        day = ''

    serializer = TimetableSerializer(qs, many=True)

    if not serializer.data:
        holiday = f'Looks like you have no lectures for {day}! <br> Go out and enjoy!'
        return Response(create_text_response(holiday), status=status.HTTP_200_OK)

    text = f"Your timetable for {day or 'the week'} is as follows:"
    table = json2html.convert(json = serializer.data)
    response = create_response([{'text':text},{'table':table}])

    return Response(response, status=status.HTTP_200_OK)


def create_response(objectArray):
    return {
        'response': objectArray
    }

def create_text_response(text):
    return {
        'response': [{
            'text': text
        }]
    }