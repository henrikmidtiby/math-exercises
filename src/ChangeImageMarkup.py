import re
import collections
import percache
import hashlib

images_uploaded_to_imgur = percache.Cache('images_on_imgur.bin', livesync=True)


Image = collections.namedtuple('Image', ['nr', 'content'])

def checksum_md5(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.digest()


class ChangeImageMarkup:
    def __init__(self):
        self.image = re.compile('(.*)\\\\image\{(.*)\}\{(.*)\}(.*)')
        self.external_url = 'https://raw.githubusercontent.com/henrikmidtiby/mathexerciseimages/master/'
        self.remove_from_relative_filename = 'mathexerciseimages/'

    def get_image_hash(self, path_to_image):
        result = {}
        result['external_path'] = "imgur:%s" % path_to_image
        try:
            result['md5checksum'] = checksum_md5(path_to_image)
        except FileNotFoundError as e:
            print("Could not open file: '%s'" % e.filename)
            result['md5checksum'] = ''
        return result

    def generator(self, input_lines):
        for line in input_lines:
            res_image = self.image.match(line)
            if res_image:
                path_to_inserted_file = res_image.group(3)
                imgur_data = self.get_image_hash(path_to_inserted_file)
                line = "{text_before_image}<img src='{fullurl}' " \
                       "'>{text_after_image}".format(
                    text_before_image=res_image.group(1),
                    fullurl=imgur_data['external_path'],
                    text_after_image=res_image.group(4),
                )
            yield line
