from django.contrib import admin
from . import models

admin.site.register(models.Candidate)
admin.site.register(models.IDCard)
admin.site.register(models.Vote)
admin.site.register(models.VoteID)