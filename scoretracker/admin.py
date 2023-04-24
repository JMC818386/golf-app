from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Hole)
admin.site.register(Round)
admin.site.register(HoleScore)

