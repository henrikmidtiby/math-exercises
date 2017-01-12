import re
import collections


Image = collections.namedtuple('Image', ['nr', 'content'])

class ChangeImageMarkup:
    def __init__(self):
        self.image = re.compile('(.*)\\\\image\{(.*)\}\{(.*)\}(.*)')
        self.external_url = 'https://raw.githubusercontent.com/henrikmidtiby/mathexerciseimages/master/'
        self.remove_from_relative_filename = 'mathexerciseimages/'

    def generator(self, input_lines):
        for line in input_lines:
            res_image = self.image.match(line)
            if res_image:
                relative_url = res_image.group(3).replace(self.remove_from_relative_filename, '')
                line = "{text_before_image}<img src='{baseurl}{relativeurl}' " \
                        "width='{image_scaling_in_percent}%'>{text_after_image}".format(
                            text_before_image=res_image.group(1),
                            baseurl=self.external_url,
                            relativeurl=relative_url,
                            image_scaling_in_percent=float(res_image.group(2))*200,
                            text_after_image=res_image.group(4),
                        )
            yield line
