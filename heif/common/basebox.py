# -----------------------------------
# import
# -----------------------------------
from common import futils

# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------

class Box:
    """
    ISO/IEC 14496-12
    """

    def __init__(self, f):
        self.start_fp = f.tell()
        # size is an integer that specifies the number of bytes in this box,
        # including all its fields and contained boxes;
        # if size is 1 then the actual size is in the field large size;
        # if size is 0, then this box is the last one in the file,
        # and its contents extend to the end of the file (normally only used for a Media Data Box)
        self.size = futils.read32(f, 'big')
        # type identifies the box type;
        # standard boxes use a compact type, which is normally four printable characters,
        # to permit ease of identification, and is shown so in the boxes below.
        # User extensions use an extended type; in this case, the type field is set to ‘uuid’.
        self.type = futils.read32(f, 'big', decode=True)
        if self.size == 1:
            self.largesize = futils.read64(f, 'big')
        elif self.size == 0:
            # box extends to end of file
            pass
        if self.type == 'uuid':
            self.usertype = [futils.read8(f, 'big') for _ in range(16)]

    def print_box(self):
        print('boxtype :', self.type)
        print('boxsize :', hex(self.size))

    def remain_size(self, f):
        return self.size - (f.tell() - self.start_fp)


class FullBox(Box):
    def __init__(self, f):
        super(FullBox, self).__init__(f)
        v_flags = futils.read32(f, 'big')
        self.version = (v_flags & 0xff000000) >> 24
        self.flags = (v_flags & 0x00ffffff)

    def print_box(self):
        super(FullBox, self).print_box()
        print('version :', self.version)
        print('flags :', self.flags)



# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass