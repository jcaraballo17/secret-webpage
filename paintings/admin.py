from django.contrib import admin
from paintings.models import Announcement, HomePageImage, Painting, Exhibition, ExhibitionImage, Video, Word


@admin.register(Announcement)
class AnnouncementsAdmin(admin.ModelAdmin):
    pass


@admin.register(HomePageImage)
class HomePageImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    pass


class ExhibitionPaintingsInline(admin.TabularInline):
    model = ExhibitionImage
    fk_name = 'exhibition'


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    inlines = [ExhibitionPaintingsInline,]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Word)
class WordsAdmin(admin.ModelAdmin):
    pass
