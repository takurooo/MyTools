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
class ItemLocationBox(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘iloc’
    Container: Meta box (‘meta’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self, f):
        super(ItemLocationBox, self).__init__(f)
        self.offset_size = None
        self.length_size = None
        self.base_offset_size = None
        self.item_count = None
        self.item_ID = None
        self.data_reference_index = None
        self.base_offset = None
        self.extent_count = None
        self.extent_offset = None
        self.extent_length = None
        self.parse(f)
        assert self.remain_size(f) == 0, '{} remainsize {} not 0.'.format(self.type, self.remain_size(f))

    def parse(self, f):

        data = futils.read16(f, 'big')
        # offset_size is taken from the set {0, 4, 8} and indicates the length in bytes of the offset field.
        self.offset_size = (data & 0x4000) >> 12
        # length_size is taken from the set {0, 4, 8} and indicates the length in bytes of the length field.
        self.length_size = (data & 0x0400) >> 8
        # base_offset_size is taken from the set {0, 4, 8} and indicates the length in bytes of the base_offset field.
        self.base_offset_size = (data & 0x0040) >> 4
        # reserved = (data & 0x0004)

        self.item_count = futils.read16(f, 'big')
        self.item_ID = []
        self.data_reference_index = []
        self.base_offset = []
        self.extent_count = []
        self.extent_offset = [[] for _ in range(self.item_count)]
        self.extent_length = [[] for _ in range(self.item_count)]
        for i in range(self.item_count):
            self.item_ID.append(futils.read16(f, 'big'))
            self.data_reference_index.append(futils.read16(f, 'big'))

            size = self.base_offset_size * 8
            if 0 < size:
                self.base_offset.append(futils.readn(f, size, 'big'))
            else:
                self.base_offset.append(0)

            self.extent_count.append(futils.read16(f, 'big'))
            for j in range(self.extent_count[-1]):
                size = self.offset_size * 8
                if 0 < size:
                    self.extent_offset[i].append(futils.readn(f, size, 'big'))
                else:
                    self.extent_offset[i].append(0)

                size = self.length_size * 8
                if 0 < size:
                    self.extent_length[i].append(futils.readn(f, size, 'big'))
                else:
                    self.extent_length[i].append(0)

    def print_box(self):
        super(ItemLocationBox, self).print_box()
        print("offset_size :", self.offset_size)
        print("length_size :", self.length_size)
        print("base_offset_size :", self.base_offset_size)
        print("item_count :", self.item_count)
        print("item_ID :", self.item_ID)
        print("data_reference_index :", self.data_reference_index)
        print("base_offset :", self.base_offset)
        print("extent_count :", self.extent_count)
        print("extent_offset :", self.extent_offset)
        print("extent_length :", self.extent_length)


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass