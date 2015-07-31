from django.db import models


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


class Piece(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateField()
    description = models.CharField(max_length=512)
    size = models.CharField(max_length=32)
    medium = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
