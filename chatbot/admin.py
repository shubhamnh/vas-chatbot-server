from django.contrib import admin
from .models import IndividualNotification, GroupNotification, Feedback, ConcessionApplication

admin.site.register(IndividualNotification)
admin.site.register(GroupNotification)
admin.site.register(Feedback)
admin.site.register(ConcessionApplication)
