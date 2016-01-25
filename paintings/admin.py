from django.contrib import admin
from paintings.models import Announcement, HomePageImage, Painting


@admin.register(Announcement)
class AnnouncementsAdmin(admin.ModelAdmin):
    pass


@admin.register(HomePageImage)
class HomePageImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    pass
