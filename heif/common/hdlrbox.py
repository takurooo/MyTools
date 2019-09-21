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
class HandlerReferenceBox(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘hdlr’
    Container: Media Box (‘mdia’) or Meta Box (‘meta’)
    Mandatory: Yes
    Quantity: Exactly one
    """

    def __init__(self, f):
        super(HandlerReferenceBox, self).__init__(f)
        self.pre_defined = None
        self.handler_type = None
        self.name = None
        self.parse(f)
        assert self.remain_size(f) == 0, '{} remainsize {} not 0.'.format(self.type, self.remain_size(f))

    def parse(self, f):
        self.pre_defined = futils.read32(f, 'big')
        self.handler_type = futils.read32(f, 'big', decode=True)
        for _ in range(3):
            _ = futils.read32(f, 'big')  # reserved
        self.name = futils.read_null_terminated(f)

    def print_box(self):
        super(HandlerReferenceBox, self).print_box()
        print("pre_defined :", self.pre_defined)
        print("handler_type :", self.handler_type)
        print("name :", self.name)

# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass