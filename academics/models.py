from django.db import models
from users.models import Teacher, Student, Class
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

SEM_CHOICES = [(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5'), (6,'6'), (7,'7'), (8,'8')]

class Course(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    acronym = models.CharField(max_length=5, blank=False, null=False)
    teacher = models.ManyToManyField(Teacher)

    def __str__(self):
        return f"{self.name} ({self.acronym})"

class TimeTable(models.Model):
    TIME_CHOICES = [
        ("08:00-09:00","08:00-09:00"),
        ("09:00-10:00","09:00-10:00"),
        ("10:00-11:00","10:00-11:00"),
        ("11:15-12:15","11:15-12:15"),
        ("12:15-13:15","12:15-13:15"),
        ("13:45-14:45","13:45-14:45"),
        ("14:45-15:45","14:45-15:45"),
        ("15:45-16:45","15:45-16:45"),
        ("16:45-17:45","16:45-17:45"),
        ("17:45-18:45","17:45-18:45"),
    ]
    WEEKDAY_CHOICES = [
        ("MON","MONDAY"),
        ("TUE","TUESDAY"),
        ("WED","WEDNESDAY"),
        ("THU","THURSDAY"),
        ("FRI","FRIDAY"),
        ("SAT","SATURDAY"),
    ]
    BATCH_CHOICES = [(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')]

    weekday = models.CharField(max_length=3, choices=WEEKDAY_CHOICES, blank=False)
    timing = models.CharField(max_length=11, choices=TIME_CHOICES, blank=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=15)
    tclass = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Class')
    batch = models.PositiveSmallIntegerField(choices=BATCH_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.tclass} - {self.weekday} - {self.timing}"
    
    class Meta:
        unique_together = (('weekday','timing','teacher','course','classroom','tclass','batch'))

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_year = models.CharField(max_length=7, verbose_name='Examination Year')
    semester = models.PositiveSmallIntegerField(choices=SEM_CHOICES)
    prac_score = models.CharField(max_length=7, verbose_name='Practical Score')
    term_score = models.CharField(max_length=7, verbose_name='Termwork Score')
    ia_score = models.CharField(max_length=7, verbose_name='Internal Assessment Score')
    ese_score = models.CharField(max_length=7, verbose_name='End Semester Exam Score')
    total_score = models.CharField(max_length=7, verbose_name='Total Score')

    def __str__(self):
        return f"{self.student.user.get_full_name()}'s {self.course} score is {self.total_score}"

    class Meta:
        verbose_name_plural = 'Marks'
        unique_together = (('student','course','semester'))

class SemesterResult(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade_point = models.DecimalField(max_digits=4, decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(10)])
    semester = models.PositiveSmallIntegerField(choices=SEM_CHOICES)
    
    @property
    def status(self):
        if self.grade_point == Decimal('0.0'):
            return 'Fail'
        return 'Pass'
    
    def __str__(self):
        return f"{self.student.user.get_full_name()}'s semester {self.semester} Grade Point is {self.grade_point}"