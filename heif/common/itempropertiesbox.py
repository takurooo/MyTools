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
class ItemProperty(Box):
    """
    ISO/IEC 23008-12
    """

    def __init__(self, f):
        super(ItemProperty, self).__init__(f)


class ItemFullProperty(FullBox):
    """
    ISO/IEC 23008-12
    """

    def __init__(self, f):
        super(ItemFullProperty, self).__init__(f)


class ItemPropertyContainerBox(Box):
    """
    ISO/IEC 23008-12
    Box Type: ‘ipco’
    """

    def __init__(self, f):
        super(ItemPropertyContainerBox, self).__init__(f)


class ItemPropertyAssociation(FullBox):
    """
    ISO/IEC 23008-12
    Box Type: ‘ipma’
    """

    def __init__(self, f):
        super(ItemPropertyAssociation, self).__init__(f)
        self.entry_cout = futils.read32(f, 'big')

        self.item_ID = []
        self.association_count = []
        self.essential = [[] for _ in range(self.entry_cout)]
        self.property_index = [[] for _ in range(self.entry_cout)]
        for i in range(self.entry_cout):
            if self.version < 1:
                self.item_ID.append(futils.read16(f, 'big'))
            else:
                self.item_ID.append(futils.read32(f, 'big'))
            self.association_count.append(futils.read8(f, 'big'))
            for _ in range(self.association_count[-1]):
                if self.flags & 1:
                    tmp = futils.read16(f, 'big')
                    self.essential[i].append((tmp & 0x8000) >> 15)
                    self.property_index.append(tmp & 0x7fff)
                else:
                    tmp = futils.read8(f, 'big')
                    self.essential[i].append((tmp & 0x80) >> 7)
                    self.property_index.append(tmp & 0x7f)


class ItemPropertiesBox(Box):
    """
    ISO/IEC 23008-12
    Box Type: ‘iprp’
    Container: Meta box (‘meta’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self, f):
        super(ItemPropertiesBox, self).__init__(f)
        self.parse(f)

    def parse(self, f):
        self.property_container = ItemPropertyContainerBox(f)


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass