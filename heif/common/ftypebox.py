# -----------------------------------
# import
# -----------------------------------
from common import futils
from common.basebox import Box, FullBox

# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------
class FileTypeBox(Box):
    """
    ISO/IEC 14496-12
    Box Type: `ftyp’
    Container: File
    Mandatory: Yes
    Quantity: Exactly one
    """

    def __init__(self, f):
        super(FileTypeBox, self).__init__(f)
        self.parse(f)
        assert self.remain_size(f) == 0, '{} remainsize {} not 0.'.format(self.type, self.remain_size(f))

    def parse(self, f):
        self.major_brand = futils.read32(f, 'big', decode=True)

        self.minor_version = futils.read32(f, 'big', decode=True)

        self.compatible_brands = []
        for _ in range(self.remain_size(f) // 4):
            self.compatible_brands.append(futils.read32(f, 'big', decode=True))

    def print_box(self):
        super(FileTypeBox, self).print_box()
        print("major_brand :", self.major_brand)
        print("minor_version :", self.minor_version)
        print("compatible_brands :", self.compatible_brands)


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass