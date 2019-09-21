# -----------------------------------
# import
# -----------------------------------
import struct

# -----------------------------------
# define
# -----------------------------------
BIG_LITTLE = {'little':'<', 'big':'>'}


# -----------------------------------
# function
# -----------------------------------


def read8(f, order='big', decode=False):
    if decode:
        return f.read(1).decode()
    else:
        return struct.unpack(BIG_LITTLE[order] + 'B', f.read(1))[0]


def read16(f, order='big', decode=False):
    if decode:
        return f.read(2).decode()
    else:
        return struct.unpack(BIG_LITTLE[order] + 'H', f.read(2))[0]


def read32(f, order='big', decode=False):
    if decode:
        return f.read(4).decode()
    else:
        return struct.unpack(BIG_LITTLE[order] + 'L', f.read(4))[0]


def read64(f, order='big', decode=False):
    if decode:
        return f.read(8).decode()
    else:
        return struct.unpack(BIG_LITTLE[order] + 'Q', f.read(8))[0]


def readn(f, size, order='big', decode=False):
    if size == 64:
        data = read64(f, order, decode)
    elif size == 32:
        data = read32(f, order, decode)
    elif size == 16:
        data = read16(f, order, decode)
    elif size == 8:
        data = read8(f, order, decode)
    else:
        raise ValueError()

    return data


def read_null_terminated(f):
    null = b'\x00'
    s = ''
    while True:
        c = read8(f, 'big', decode=True)
        s += c
        if c.encode() == null:
            break
    return s


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
