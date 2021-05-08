from django.db import models
from users.models import Student, Teacher, Class, Interest

class IndividualNotification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    notice = models.CharField(max_length=500)
    visited = models.BooleanField(default=False)
    modified_date = models.DateField(auto_now=True)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject}"


class GroupNotification(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    notice = models.CharField(max_length=500)
    nclass = models.ForeignKey(Class, on_delete=models.PROTECT, verbose_name='Class')
    interest = models.ForeignKey(Interest, on_delete=models.PROTECT)
    modified_date = models.DateField(auto_now=True)
    creation_date = models.DateField(auto_now_add=True)
    # attachment = models.FileField(null=True)
    # filename = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.subject}"

class Feedback(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    subject = models.CharField(max_length=100)
    details = models.CharField(max_length=500)
    status = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.subject

class ConcessionApplication(models.Model):
    DURATION_CHOICES = [ ('MON','MONTHLY'), ('QTY','QUATERLY'), ]
    CLASS_CHOICES = [ ('FC','FIRST CLASS'), ('SC','SECOND CLASS'), ]
    APPLICATION_STATUS = [ ('NEW','NEW'), ('APR','APPROVE'), ('CAN','CANCEL')]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_station = models.CharField(max_length=20)
    to_station = models.CharField(max_length=20)
    duration = models.CharField(max_length=3, choices=DURATION_CHOICES, default='MON')
    train_class = models.CharField(max_length=2, choices=CLASS_CHOICES, default='SC')
    prev_ticket_no = models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=3, choices=APPLICATION_STATUS, default='NEW')
    modified_date = models.DateField(auto_now=True)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student}'s Application"