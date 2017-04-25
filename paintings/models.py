import re

from PIL import Image, ImageOps
from django.core.exceptions import ValidationError

from django.db import models
from imagekit.models.fields import ImageSpecField

from paintings.image_processors import RelativeResize, Thumbnail


class Piece(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order',)
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

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class ImagePiece(models.Model):
    # TODO: sizes should be changed in an admin form. maybe.
    PREVIEW_MAX_SIZE = 720
    ORIGINAL_MAX_SIZE = 1600
    upload_directory = ''

    image = models.ImageField(upload_to=upload_directory)
    image_thumbnail = ImageSpecField(source='image', format='JPEG', options={'quality': 80}, processors=[Thumbnail(300, 300)])
    image_preview = ImageSpecField(source='image', format='JPEG', options={'quality': 90}, processors=[RelativeResize(PREVIEW_MAX_SIZE)])

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(ImagePiece, self).save(*args, **kwargs)
        uploaded_image = Image.open(self.image.path)
        image_size = RelativeResize.get_new_size(self.image, self.ORIGINAL_MAX_SIZE)
        uploaded_image = uploaded_image.resize(image_size, Image.ANTIALIAS)
        uploaded_image.save(self.image.path)


class HomePageImage(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='home_images')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Announcement(Piece):
    short_description = models.CharField(max_length=1024)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.active:
            active_announcements = Announcement.objects.filter(active=True)
            for announcement in active_announcements:
                announcement.active = False
                announcement.save()

        return super(Announcement, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Painting(Piece, ImagePiece):
    upload_directory = 'paintings'
    medium = models.CharField(max_length=128, null=True, blank=True)
    size = models.CharField(max_length=32, null=True, blank=True)


class Exhibition(Piece):
    thumbnail_upload_directory = 'exhibition_thumbnails'
    place = models.CharField(max_length=256, default='', null=True, blank=True)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_directory, null=True, blank=True)
    exhibition_thumbnail = ImageSpecField(source='thumbnail', format='JPEG', options={'quality': 80}, processors=[Thumbnail(385, 385)])


class ExhibitionImage(ImagePiece):
    upload_directory = 'exhibition_paintings'
    caption = models.CharField(max_length=256, default='', null=True, blank=True)
    exhibition = models.ForeignKey(Exhibition, related_name='images')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order', )


class Video(Piece):
    video_link = models.URLField()

    def clean(self):
        super(Video, self).clean()
        if not self.youtube_url_validation(self.video_link):
            raise ValidationError({'video_link': 'Must be a Youtube video.'})

    @staticmethod
    def youtube_url_validation(url):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        youtube_regex_match = re.match(youtube_regex, url)
        if youtube_regex_match:
            return youtube_regex_match.group(6)

        return youtube_regex_match


class Word(models.Model):
    title = models.CharField(max_length=1024)
    content = models.TextField()
    featured = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order', )

    def save(self, *args, **kwargs):
        if self.featured:
            previous_featured_queryset = Word.objects.filter(featured=True)
            if previous_featured_queryset.exists():
                previous_featured = previous_featured_queryset.get()
                previous_featured.featured = False
                previous_featured.save()

        return super(Word, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
