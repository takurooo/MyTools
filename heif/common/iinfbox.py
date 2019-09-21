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
class ItemInfoExtension:
    def __init__(self, extension_type):
        pass


class ItemInfoEntry(FullBox):
    def __init__(self, f):
        super(ItemInfoEntry, self).__init__(f)
        self.item_ID = None
        self.item_protection_index = None
        self.item_name = None
        self.item_type = None
        self.item_uri_type = None
        self.content_type = None
        self.content_encoding = None
        self.extension_type = None
        self.iteminfoext = None
        self.parse(f)

    def parse(self, f):

        if self.version == 0 or self.version == 1:
            self.item_ID = futils.read16(f, 'big')
            self.item_protection_index = futils.read16(f, 'big')
            self.item_name = futils.read_null_terminated(f)
            self.content_type = futils.read_null_terminated(f)

            if 0 < self.remain_size(f):
                self.content_encoding = futils.read_null_terminated(f)  # optional

            if self.version == 1 and 0 < self.remain_size(f):
                self.extension_type = futils.read32(f, 'big')  # optional
                self.iteminfoext = ItemInfoExtension(self.extension_type)  # optional

        if self.version >= 2:
            if self.version == 2:
                self.item_ID = futils.read16(f, 'big')
            elif self.version == 3:
                self.item_ID = futils.read32(f, 'big')

            self.item_protection_index = futils.read16(f, 'big')
            self.item_type = futils.read32(f, 'big', decode=True)

            self.item_name = futils.read_null_terminated(f)
            if self.item_name == 'mine':
                self.content_type = futils.read_null_terminated(f)
                if 0 < self.remain_size(f):
                    self.content_encoding = futils.read_null_terminated(f) # optional
            elif self.item_type == 'uri ':
                self.item_uri_type = futils.read_null_terminated(f)

    def print_box(self):
        super(ItemInfoEntry, self).print_box()
        print("item_ID :", self.item_ID)
        print("item_protection_index :", self.item_protection_index)
        print("item_name :", self.item_name)
        print("item_type :", self.item_type)
        print("item_uri_type :", self.item_uri_type)
        print("content_type :", self.content_type)
        print("content_encoding :", self.content_encoding)
        print("extension_type :", self.extension_type)


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
        assert self.remain_size(f) == 0, '{} remainsize {} not 0.'.format(self.type, self.remain_size(f))

    def parse(self, f):
        if self.version == 0:
            self.entry_count = futils.read16(f, 'big')
        else:
            self.entry_count = futils.read32(f, 'big')

        self.infe = [ItemInfoEntry(f) for _ in range(self.entry_count)]

    def print_box(self):
        super(ItemInformationBox, self).print_box()
        print("entry_count :", self.entry_count)
        for i in range(self.entry_count):
            self.infe[i].print_box()


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass