from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(TimeTable)
admin.site.register(Marks)
admin.site.register(SemesterResult)