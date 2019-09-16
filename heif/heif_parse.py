# -----------------------------------
# import
# -----------------------------------
import os
import argparse
from common.boxreader import BoxReader

# -----------------------------------
# define
# -----------------------------------


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

    box_reader = BoxReader(img_path)
    boxtype_list = box_reader.read_boxes()
    print(boxtype_list)

    iloc = box_reader.get_box('iloc')
    iloc.print_box()

    ftyp = box_reader.get_box('ftyp')
    ftyp.print_box()

    hdlr = box_reader.get_box('hdlr')
    hdlr.print_box()

    iinf = box_reader.get_box('iinf')
    iinf.print_box()


if __name__ == '__main__':
    main(get_args())
