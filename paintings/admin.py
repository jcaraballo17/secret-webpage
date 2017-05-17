from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from paintings.models import Announcement, HomePageBackground, Painting, Exhibition, ExhibitionImage, Video, Word


@admin.register(Announcement)
class AnnouncementsAdmin(admin.ModelAdmin):
    pass


@admin.register(HomePageBackground)
class HomePageImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Painting)
class PaintingAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display_links = None


class ExhibitionPaintingsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ExhibitionImage
    list_display_links = None
    list_display = ('', )


@admin.register(Exhibition)
class ExhibitionAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [ExhibitionPaintingsInline, ]
    list_display_links = None


@admin.register(Video)
class VideoAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display_links = None


@admin.register(Word)
class WordsAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display_links = None
