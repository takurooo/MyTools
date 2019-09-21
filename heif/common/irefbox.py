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


class SingleItemTypeReferenceBox(Box):
    def __init__(self, f):
        super(SingleItemTypeReferenceBox, self).__init__(f)
        self.from_item_ID = None
        self.reference_count = None
        self.to_item_ID = None
        self.parse(f)

    def parse(self, f):
        self.from_item_ID = futils.read16(f, 'big')
        self.reference_count = futils.read16(f, 'big')
        self.to_item_ID = []
        for _ in range(self.reference_count):
            self.to_item_ID.append(futils.read16(f, 'big'))

    def print_box(self):
        super(SingleItemTypeReferenceBox, self).print_box()
        print("from_item_ID :", self.from_item_ID)
        print("reference_count :", self.reference_count)
        print("to_item_ID :", self.to_item_ID)


class SingleItemTypeReferenceBoxLarge(Box):
    def __init__(self, f):
        super(SingleItemTypeReferenceBoxLarge, self).__init__(f)
        self.from_item_ID = None
        self.reference_count = None
        self.to_item_ID = None
        self.parse(f)

    def parse(self, f):
        self.from_item_ID = futils.read32(f, 'big')
        self.reference_count = futils.read16(f, 'big')
        self.to_item_ID = []
        for _ in range(self.reference_count):
            self.to_item_ID.append(futils.read32(f, 'big'))

    def print_box(self):
        super(SingleItemTypeReferenceBoxLarge, self).print_box()
        print("from_item_ID :", self.from_item_ID)
        print("reference_count :", self.reference_count)
        print("to_item_ID :", self.to_item_ID)


class ItemReferenceBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘iref’
    Container:  Metadata	box	(‘meta’)
    Mandatory:  No
    Quantity:   Zero	or	one
    """

    def __init__(self, f):
        super(ItemReferenceBox, self).__init__(f)
        self.references = None
        self.parse(f)

    def parse(self, f):
        self.references = []
        while 0 < self.remain_size(f):
            if self.version == 0:
                self.references.append(SingleItemTypeReferenceBox(f))
            else:
                self.references.append(SingleItemTypeReferenceBoxLarge(f))

    def print_box(self):
        super(ItemReferenceBox, self).print_box()
        for reference in self.references:
            reference.print_box()


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
