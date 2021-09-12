from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.fields import CurrentUserDefault

from django.db import models
from users.models import Student, Interest, InterestStatus
from chatbot.models import Feedback, IndividualNotification, GroupNotification

class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name')
    current_class = serializers.CharField(source='current_class.__str__')

    class Meta:
        model = Student
        fields = ('name', 'current_class', 'batch',)

class InterestStatusSerializer(serializers.ModelSerializer):
    interest_id = serializers.IntegerField(source='interest.id')
    name = serializers.CharField(source='interest.name')

    class Meta:
        model = InterestStatus
        fields = ('interest_id','name','status',)
        read_only_fields = ('interest_id','name',)
        extra_kwargs = {'status': {'required': True}}

class SettingsSerializer(serializers.ModelSerializer):
    interests = InterestStatusSerializer(many=True)

    class Meta:
        model = Student
        fields = ('batch','interests')

    def validate(self, data):
        # Validate id and interest name combination
        user_interests = data['interests']
        for x in range(len(user_interests)):
            interest_id = user_interests[x].get('interest').get('id')
            name = user_interests[x].get('interest').get('name')
            
            # TO DO - Check db hits
            if not Interest.objects.filter(id__exact=interest_id, name__exact=name).exists():
                raise serializers.ValidationError(f"Could not find Interest with interest_id '{interest_id}' and name '{name}'.")

        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        # OrderedDict of interests
        changed_interests = validated_data.pop('interests')
        user = validated_data["user"]

        # Update interests
        for changed_interest in changed_interests:
            interest_id = changed_interest.get('interest').get('id')
            status = changed_interest.get('status')

            try:
                interest_instance = instance.interests.get(interest__id=interest_id)
                interest_instance.status = changed_interest.get('status', interest_instance.status)
                interest_instance.save()
            except InterestStatus.DoesNotExist:
                InterestStatus.objects.create(student=user.student, interest_id=interest_id, status=status)

        # Update batch (Student Model)
        return super().update(instance, validated_data)

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('subject', 'details')

    def create(self, validated_data):
        student = self.context['request'].user.student
        feedback = Feedback.objects.create(student=student, **validated_data)
        return feedback

class IndividualNotificationSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(source='teacher.user.get_full_name')

    class Meta:
        model = IndividualNotification
        fields = ('teacher', 'subject', 'notice', 'creation_date')

class GroupNotificationSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(source='teacher.user.get_full_name')
    interest = serializers.CharField(source='interest.name')

    class Meta:
        model = GroupNotification
        fields = ('teacher','subject','notice','interest', 'creation_date')

class QuerySerializer(serializers.Serializer):
    """Query Serializer"""

    query = serializers.CharField(allow_blank=False)