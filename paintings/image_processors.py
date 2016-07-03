from pilkit.processors.base import Anchor
from pilkit.processors.resize import Resize, Thumbnail


# Image processor for paintings

class RelativeResize(object):
    def __init__(self, max_size, upscale=True, anchor=Anchor.CENTER):
        self.max_size = max_size
        self.upscale = upscale
        self.anchor = anchor

    @classmethod
    def get_new_size(cls, image, max_size):
        is_landscape = image.width > image.height
        width = int(round(max_size if is_landscape else (float(image.width) / image.height) * max_size))
        height = int(round(max_size if not is_landscape else (float(image.height) / image.width) * max_size))
        return width, height

    def process(self, image):
        width, height = RelativeResize.get_new_size(image, self.max_size)
        image = Resize(width, height, upscale=self.upscale).process(image)
        return image