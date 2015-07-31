from django.contrib import admin
from paintings.models import Announcement


@admin.register(Announcement)
class AnnouncementsAdmin(admin.ModelAdmin):
    pass
