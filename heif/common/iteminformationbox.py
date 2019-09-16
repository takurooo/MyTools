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
class ItemInfoEntry(FullBox):
    def __init__(self, f):
        super(ItemInfoEntry, self).__init__(f)
        self.parse(f)

    def parse(self, f):
        self.item_ID = futils.read16(f, 'big')
        self.item_protection_index = futils.read16(f, 'big')

        self.item_name = futils.read_null_terminated(f)
        self.content_type = futils.read_null_terminated(f)

        self.content_encoding = None
        if 0 < self.remain_size(f):
            self.content_encoding = futils.read_null_terminated(f)

    def print_box(self):
        print()
        super(ItemInfoEntry, self).print_box()
        print("item_ID :", self.item_ID)
        print("item_protection_index :", self.item_protection_index)
        print("item_name :", self.item_name)
        print("content_type :", self.content_type)
        print("content_encoding :", self.content_encoding)


class ItemInformationBox(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘iinf’
    Container: Meta Box (‘meta’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self, f):
        super(ItemInformationBox, self).__init__(f)
        self.parse(f)
        assert self.remain_size(f) == 0, 'remainsize {} not 0.'.format(self.remain_size(f))

    def parse(self, f):
        self.entry_count = futils.read16(f, 'big')
        self.infe = [ItemInfoEntry(f) for _ in range(self.entry_count)]

    def print_box(self):
        print()
        super(ItemInformationBox, self).print_box()
        print("entry_count :", self.entry_count)
        for i in range(self.entry_count):
            self.infe[i].print_box()


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass