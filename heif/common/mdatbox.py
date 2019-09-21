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
class MediaDataBox(Box):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘mdat’
    Container:   File
    Mandatory:   No
    Quantity:   Zero	or	more
    """

    def __init__(self, f):
        super(MediaDataBox, self).__init__(f)
        self.skip_to_end(f)

    def print_box(self):
        super(MediaDataBox, self).print_box()


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
