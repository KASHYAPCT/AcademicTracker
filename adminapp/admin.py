from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Timetable)
admin.site.register(Notifications)
admin.site.register(StudentResult)



