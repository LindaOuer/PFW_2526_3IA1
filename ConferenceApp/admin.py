from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Conference)
admin.site.register(Submission)
admin.site.register(OrganizingCommittee)