from PIL import Image, ImageOps

from django.db import models
from imagekit.models.fields import ImageSpecField

from paintings.image_processors import RelativeResize, Thumbnail


class Piece(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateField()
    description = models.CharField(max_length=512)

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

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class ImagePiece(models.Model):
    # TODO: sizes should be changed in an admin form. maybe.
    PREVIEW_MAX_SIZE = 720
    ORIGINAL_MAX_SIZE = 1600

    upload_directory = ''
    size = models.CharField(max_length=32)

    image = models.ImageField(upload_to=upload_directory)
    image_thumbnail = ImageSpecField(source='image', format='JPEG', options={'quality': 80},
                                     processors=[Thumbnail(300, 300)])
    image_preview = ImageSpecField(source='image', format='JPEG', options={'quality': 90},
                                   processors=[RelativeResize(PREVIEW_MAX_SIZE)])

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


class Announcement(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    short_description = models.CharField(max_length=1024)
    active = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.active:
            active_announcements = Announcement.objects.filter(active=True)
            for announcement in active_announcements:
                announcement.active = False
                announcement.save()

        super(Announcement, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Exhibition(Piece):
    place = models.CharField(max_length=256, default='')


class ExhibitionPainting(ImagePiece):
    upload_directory = 'exhibition_paintings'
    exhibition = models.ForeignKey(Exhibition, related_name='images')


class Video(Piece):
    video_link = models.URLField()


class Painting(ImagePiece):
    upload_directory = 'paintings'
    medium = models.CharField(max_length=128)
