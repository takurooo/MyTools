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
class PrimaryItemBox(FullBox):
    """
    Box Type: ‘pitm’
    Container: Meta box (‘meta’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self, f):
        super(PrimaryItemBox, self).__init__()
        self.parse(f)
        assert self.remain_size(f) == 0, 'remainsize {} not 0.'.format(self.remain_size(f))

    def parse(self, f):
        self.item_ID = futils.read16(f, 'big')

    def print_box(self):
        print()
        super(PrimaryItemBox, self).print_box()
        print('item_ID :', self.item_ID)


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass