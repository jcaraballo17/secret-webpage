import os
import re

import datetime
from PIL import Image, ImageOps
from django.core.exceptions import ValidationError

from django.db import models
from django.utils.six import python_2_unicode_compatible
from imagekit.models.fields import ImageSpecField
from embed_video.fields import EmbedVideoField

from paintings.image_processors import RelativeResize, Thumbnail


def rename_image_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    instance_class = instance.__class__.__name__.lower()
    image_name = instance.__str__().replace(' ', '-').lower()
    filename = 'woody-shepherd-%s-%s.%s' % (instance_class, image_name, extension)

    # return the whole path to the file
    return os.path.join(instance_class, filename)


class SortablePiece(models.Model):
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

    def get_next_by_field(self, field):
        next_object = None

        try:
            next_object = self._get_next_or_previous_by_FIELD(field, True)
        except self.__class__.DoesNotExist:
            pass

        return next_object

    def get_previous_by_field(self, field):
        previous_object = None

        try:
            previous_object = self._get_next_or_previous_by_FIELD(field, False)
        except self.__class__.DoesNotExist:
            pass

        return previous_object


class VisualPiece(models.Model):
    # TODO: sizes should be changed in an admin form. maybe.
    PREVIEW_MAX_SIZE = 720
    ORIGINAL_MAX_SIZE = 1600

    image = models.ImageField(upload_to=rename_image_path)
    image_thumbnail = ImageSpecField(source='image', format='JPEG', options={'quality': 80}, processors=[Thumbnail(300, 300)])
    image_preview = ImageSpecField(source='image', format='JPEG', options={'quality': 90}, processors=[RelativeResize(PREVIEW_MAX_SIZE)])

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(VisualPiece, self).save(*args, **kwargs)
        uploaded_image = Image.open(self.image.path)
        image_size = RelativeResize.get_new_size(self.image, self.ORIGINAL_MAX_SIZE)
        uploaded_image = uploaded_image.resize(image_size, Image.ANTIALIAS)
        uploaded_image.save(self.image.path)


@python_2_unicode_compatible
class HomePageBackground(models.Model):
    name = models.CharField(max_length=256, help_text='Name to identify the background with.')
    image = models.ImageField(upload_to=rename_image_path)

    class Meta:
        db_table = 'homepage_background'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Announcement(models.Model):
    title = models.CharField(max_length=256)
    short_description = models.CharField(max_length=1024, help_text='Message that will appear in the homepage announcement section.')
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    description = models.TextField(null=True, blank=True, help_text='Full announcement text with more details.')
    active = models.BooleanField(default=True, help_text='Make this the active announcement on the homepage.')

    class Meta:
        db_table = 'announcements'

    def save(self, *args, **kwargs):
        if self.active:
            active_announcement = Announcement.objects.filter(active=True).first()
            if active_announcement:
                active_announcement.active = False
                active_announcement.save()

        return super(Announcement, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Painting(SortablePiece, VisualPiece):
    title = models.CharField(max_length=256)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    medium = models.CharField(max_length=128, null=True, blank=True)
    size = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'paintings'
        ordering = ('order',)


    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Exhibition(SortablePiece):
    title = models.CharField(max_length=256)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    place = models.CharField(max_length=256, default='', null=True, blank=True)

    class Meta:
        db_table = 'exhibitions'
        ordering = ('order',)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class ExhibitionImage(SortablePiece, VisualPiece):
    caption = models.CharField(max_length=256, default='', null=True, blank=True, help_text='Optional: Caption for the photo.')
    exhibition = models.ForeignKey(Exhibition, related_name='images')

    class Meta:
        db_table = 'exhibition_images'
        ordering = ('order',)

    def __str__(self):
        return '%s photo %s' % (self.exhibition.title, self.caption or ''.join(self.image.name.split('.')[:-1]))


@python_2_unicode_compatible
class Video(SortablePiece):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    video_link = EmbedVideoField()

    class Meta:
        db_table = 'videos'
        ordering = ('order',)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Word(SortablePiece):
    title = models.CharField(max_length=1024)
    content = models.TextField()
    featured = models.BooleanField(default=False, help_text='Make this the default entry.')
    sticky = models.BooleanField(default=False, help_text='Stick to the top of the list of entries.')

    class Meta:
        db_table = 'words'
        ordering = ('order',)

    def save(self, *args, **kwargs):
        if self.featured:
            previous_featured = Word.objects.filter(featured=True).first()
            if previous_featured:
                previous_featured.featured = False
                previous_featured.save()

        return super(Word, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
