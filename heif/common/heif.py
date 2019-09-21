# -----------------------------------
# import
# -----------------------------------
from common.boxreader import BoxReader

# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------


class HeifReader:

    def __init__(self, img_path):
        self.img_path = img_path
        self.box_reader = BoxReader(self.img_path)
        self.boxtype_list = self.box_reader.read_boxes()

    def print_boxes(self):
        print("found boxes : "+ " ".join(self.boxtype_list))
        for boxtype in self.boxtype_list:
            box = self.box_reader.get_box(boxtype)
            print()
            print()
            if box is None:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("{} not support".format(boxtype))
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
                continue
            try:
                box.print_box()
            except Exception as e:
                print(boxtype, e)

# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass