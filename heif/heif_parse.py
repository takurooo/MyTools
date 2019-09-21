# -----------------------------------
# import
# -----------------------------------
import os
import argparse
from common.heif import HeifReader

# -----------------------------------
# define
# -----------------------------------
CUR_PATH = os.path.join(os.path.dirname(__file__))
JSON_PATH = os.path.join(CUR_PATH, 'config.json')

# -----------------------------------
# function
# -----------------------------------

def get_args():
    parser = argparse.ArgumentParser(description="HEIF parser.")
    parser.add_argument("img_path", type=str, help="path2your_image", default=None)
    return parser.parse_args()


# -----------------------------------
# main
# -----------------------------------
def main(args):
    img_path = args.img_path

    heif_reader = HeifReader(img_path)
    heif_reader.print_boxes()


if __name__ == '__main__':
    main(get_args())
