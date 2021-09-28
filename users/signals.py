from .models import Student, Interest, InterestStatus
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Student)
@receiver(post_save, sender=Interest)
def create_interest_status(sender, instance, created, **kwargs):
    if created:
        if sender == Student:
            interests = Interest.objects.all()
            interest_status_objs = (InterestStatus(student=instance, interest=i) for i in interests)
            InterestStatus.objects.bulk_create(interest_status_objs)

        elif sender == Interest:
            students = Student.objects.all()
            interest_status_objs = (InterestStatus(student=student, interest=instance) for student in students)
            InterestStatus.objects.bulk_create(interest_status_objs)
