"""
Renderer

Handle assembling an output image, any chrome, and displaying/saving
accordingly.
"""

import random
import string

from PIL import Image


class Renderer:
    """This class renders lists of images and their pixel locations."""
    def __init__(self, image_pixel_list=None):
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.image_pixel_list = []
        if image_pixel_list is not None:
            self.add_image_pixel_list(image_pixel_list)

    def initialise_image(self, width, height):
        """Set up a clean image"""
        self.image = Image.new('RGBA', (width, height), (255, 0, 0, 0))

    def add_image_pixel_list(self, image_pixel_list):
        """Add some images at some series of offsets to the list of images to
         be rendered"""
        for sub_image, x, y in image_pixel_list:
            min_x, min_y, max_x, max_y = \
                self.get_image_pixel_boundaries(sub_image, x, y)
            self.min_x = min(min_x, self.min_x)
            self.min_y = min(min_y, self.min_y)
            self.max_x = max(max_x, self.max_x)
            self.max_y = max(max_y, self.max_y)

        self.image_pixel_list = image_pixel_list+self.image_pixel_list

    def add_to_image(self, sub_image, x, y):
        """Adds all images to the final picture, taking into account their
         top-left corner offsets"""
        final_x = x-sub_image.top_left["x"]
        final_y = y-sub_image.top_left["y"]
        # second image.image call is alpha mask.
        self.image.paste(sub_image.image, (final_x, final_y), sub_image.image)

    @staticmethod
    def get_image_pixel_boundaries(sub_image, x, y):
        min_x = x-sub_image.top_left["x"]
        min_y = y-sub_image.top_left["y"]
        max_x = min_x+sub_image.image.width
        max_y = min_y+sub_image.image.height
        return (min_x, min_y, max_x, max_y)

    def assemble(self):
        """Initialise and populate the final image"""
        image_pixel_width = self.max_x - self.min_x + 20
        image_pixel_height = self.max_y - self.min_y + 20
        self.initialise_image(image_pixel_width, image_pixel_height)
        for sub_image, x, y in self.image_pixel_list:
            self.add_to_image(sub_image, x-self.min_x+10, y-self.min_y+10)

    def output(self, destination, filename=None):
        """Actually put the image somewhere"""

        self.assemble()

        if destination == 'screen':
            self.image.show()
        elif destination == 'file':
            if not filename:
                filename = ''.join([random.SystemRandom()
                                   .choice(string.ascii_lowercase)
                                   for n in range(8)])
            self.image.save('output/' + filename + ".png", "PNG")
        elif destination == 'dryrun':
            # This doesn't actually do anything, but is handy for testing there
            # are no material errors.
            return
        else:
            raise ValueError("Invalid output destination '{}'"
                             .format(destination))