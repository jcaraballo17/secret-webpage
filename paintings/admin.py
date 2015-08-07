from django.contrib import admin
from paintings.models import Announcement, HomePageImage, Piece


@admin.register(Announcement)
class AnnouncementsAdmin(admin.ModelAdmin):
    pass


@admin.register(HomePageImage)
class HomePageImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    pass