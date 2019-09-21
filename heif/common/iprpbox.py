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
        self.skip_to_end(f)  # TODO

    def print_box(self):
        super(ItemProperty, self).print_box()


class ItemFullProperty(FullBox):
    """
    ISO/IEC 23008-12
    """

    def __init__(self, f):
        super(ItemFullProperty, self).__init__(f)
        self.skip_to_end()  # TODO

    def print_box(self):
        super(ItemFullProperty, self).print_box()


class ItemPropertyContainerBox(Box):
    """
    ISO/IEC 23008-12
    Box Type: ‘ipco’
    """

    def __init__(self, f):
        super(ItemPropertyContainerBox, self).__init__(f)
        self.item_properties = None
        self.parse(f)
        assert self.remain_size(f) == 0, '{} remainsize {} not 0.'.format(self.type, self.remain_size(f))

    def parse(self, f):
        self.item_properties = []
        while 0 < self.remain_size(f):
            item_property = ItemProperty(f)  # TODO
            self.item_properties.append(item_property)

    def print_box(self):
        super(ItemPropertyContainerBox, self).print_box()
        for item_property in self.item_properties:
            item_property.print_box()


class ItemPropertyAssociation(FullBox):
    """
    ISO/IEC 23008-12
    Box Type: ‘ipma’
    """

    def __init__(self, f):
        super(ItemPropertyAssociation, self).__init__(f)
        self.entry_cout = None
        self.item_ID = None
        self.association_count = None
        self.essential = None
        self.property_index = None
        self.parse(f)
        assert self.remain_size(f) == 0, '{} remainsize {} not 0.'.format(self.type, self.remain_size(f))

    def parse(self, f):
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
                    self.property_index[i].append(tmp & 0x7fff)
                else:
                    tmp = futils.read8(f, 'big')
                    self.essential[i].append((tmp & 0x80) >> 7)
                    self.property_index[i].append(tmp & 0x7f)

    def print_box(self):
        super(ItemPropertyAssociation, self).print_box()
        print("entry_cout :", self.entry_cout)
        print("item_ID :", self.item_ID)
        print("association_count :", self.association_count)
        print("essential :", self.essential)
        print("property_index :", self.property_index)


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
        self.property_container = None
        self.parse(f)
        # assert self.remain_size(f) == 0, '{} remainsize {} not 0.'.format(self.type, self.remain_size(f))

    def parse(self, f):
        self.ipco = ItemPropertyContainerBox(f)
        self.ipma = ItemPropertyAssociation(f)

    def print_box(self):
        super(ItemPropertiesBox, self).print_box()
        self.ipco.print_box()
        self.ipma.print_box()


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
