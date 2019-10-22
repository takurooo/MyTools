# -----------------------------------
# import
# -----------------------------------
import os
import argparse
from collections import OrderedDict

from common.exif_reader import ExifReader


# -----------------------------------
# define
# -----------------------------------


# -----------------------------------
# class
# -----------------------------------


# -----------------------------------
# function
# -----------------------------------
def get_args():
    parser = argparse.ArgumentParser(description="HEIF parser.")
    parser.add_argument("img_path", type=str, help="path2your_image", default=None)
    return parser.parse_args()


def get_exif_with_PIL(file_path):
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    img = Image.open(file_path)
    exif = img._getexif()

    exif_data = OrderedDict()
    for id, v in exif.items():
        exif_data[TAGS.get(id, id)] = v

    return exif_data


def test(file_path):
    # #
    # PILの結果と比較
    reference = get_exif_with_PIL(file_path)

    exif_reader = ExifReader(file_path)
    exif_list = exif_reader.get_exif()
    exif = exif_list[0]

    print('reference  tag len :', len(reference))
    print('ExifReader tag len :', len(exif))

    for tag_name, tag in exif.items():
        ref = reference.get(tag_name, None)
        if ref is not None:
            if tag.val != ref:
                print("NG : ", tag_name)
                print('    reference  :', ref)
                print('    read value :', tag.val)


# -----------------------------------
# main
# -----------------------------------
def main(args):
    exif_reader = ExifReader(args.img_path)
    exif_reader.print_log()
    exif_reader.save_log('exif.html')

    # test(args.img_path)


if __name__ == '__main__':
    main(get_args())
