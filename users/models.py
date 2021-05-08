from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.username

class Class(models.Model):
    BRANCH_CHOICES = [
        ('CMPN','Computer Engineering'),
        ('INFT','Information Technology'),
        ('EXTC','Electronics and Telecommunication Engineering'),
        ('ETRX','Electronics'),
    ]
    SEM_CHOICES = [(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5'), (6,'6'), (7,'7'), (8,'8')]
    DIV_CHOICES = [('A','A'), ('B','B'), ('C','C')]
    
    branch = models.CharField(max_length=4, choices=BRANCH_CHOICES, default='CMPN')
    semester = models.PositiveSmallIntegerField(choices=SEM_CHOICES, default=1)
    division = models.CharField(max_length=1, choices=DIV_CHOICES, default='A')

    @property
    def eng_year(self):
        if self.semester <= 2:
            return 'FY'
        elif self.semester <= 4:
            return 'SY'
        elif self.semester <= 6:
            return 'TY'
        else:
            return 'BE'
    
    def __str__(self):
        return f"{self.branch} - {self.division} (Sem {self.semester})"

    class Meta:
        verbose_name_plural = 'Classes'
        unique_together = (('branch','division','semester'),)

class Student(models.Model):
    BATCH_CHOICES = [(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_class = models.ForeignKey(Class, on_delete=models.PROTECT)
    batch = models.PositiveSmallIntegerField(choices=BATCH_CHOICES, default=1)
    address = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acronym = models.CharField(max_length=4)
    designation = models.CharField(max_length=50)

    def __str__(self):
        return self.user.get_full_name()

class Interest(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class InterestStatus(models.Model):
    student = models.ForeignKey(Student,  related_name='interests', on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, related_name='interests', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Interest Status'
        unique_together = (('student','interest'))

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.interest.name} - {self.status}"

# class Interest(models.Model):
#     student = models.OneToOneField(Student, on_delete=models.CASCADE)
#     workshop = models.BooleanField(default=True)
#     sports = models.BooleanField(default=True)
#     creative = models.BooleanField(default=True)
#     cultural = models.BooleanField(default=True)
#     placement = models.BooleanField(default=True)
#     dance = models.BooleanField(default=True)
#     drama = models.BooleanField(default=True)
#     study = models.BooleanField(default=True)

#     def __str__(self):
#         return self.student.user.get_full_name() + '\'s Interests'

#     class Meta:
#         verbose_name_plural = 'Interests'