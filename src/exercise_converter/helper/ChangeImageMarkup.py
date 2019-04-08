import os
import re
import collections
import percache
import hashlib
import pyimgur

try:
    CLIENT_ID = os.environ['IMGUR_CLIENT_ID']
    UPLOAD_IMAGES_TO_IMGUR = True
except KeyError:
    CLIENT_ID = None
    UPLOAD_IMAGES_TO_IMGUR = False


if UPLOAD_IMAGES_TO_IMGUR:
    imgur_upload_cache = percache.Cache('images_on_imgur.bin', livesync=True)
else:
    def imgur_upload_cache(func):
        def wrapper():
            func()
        return wrapper


Image = collections.namedtuple('Image', ['nr', 'content'])


def checksum_md5(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.digest()


def get_image_data(path_to_image):
    result = {}
    result['path'] = path_to_image
    try:
        result['md5checksum'] = checksum_md5(path_to_image)
    except FileNotFoundError as e:
        print("Could not open file: '%s'" % e.filename)
        result['md5checksum'] = ''
    return result


@imgur_upload_cache
def upload_to_imgur(image_information):
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(image_information['path'], title=image_information['path'])
    image_information['link'] = uploaded_image.link
    return image_information


class ChangeImageMarkup:
    def __init__(self):
        self.image = re.compile('(.*)\\\\image{(.*)}(.*)')
        self.external_url = 'https://raw.githubusercontent.com/henrikmidtiby/mathexerciseimages/master/'

    def generator(self, input_lines):
        for line in input_lines:
            res_image = self.image.match(line)
            if res_image:
                assert UPLOAD_IMAGES_TO_IMGUR, ("Not configured to upload "
                        "images to IMGUR. To configure this, set the environment "
                        "variable IMGUR_CLIENT_ID to the app secret from "
                        "imgur.com.")
                path_to_inserted_file = res_image.group(2)
                image_data = get_image_data(path_to_inserted_file)
                image_data = upload_to_imgur(image_data)
                print(image_data)
                line = "{text_before_image}![]({fullurl}) " \
                       "{text_after_image}\n".format(
                    text_before_image=res_image.group(1),
                    fullurl=image_data['link'],
                    text_after_image=res_image.group(3),
                )
            yield line

