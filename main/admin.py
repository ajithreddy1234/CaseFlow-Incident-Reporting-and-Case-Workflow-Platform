from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserCrimeReport)
admin.site.register(EvidencePhoto)
admin.site.register(Alerts)
admin.site.register(EvidenceVideo)
admin.site.register(EvidenceAudio)