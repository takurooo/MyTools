# -----------------------------------
# import
# -----------------------------------
import struct


# -----------------------------------
# define
# -----------------------------------


# -----------------------------------
# function
# -----------------------------------


def read8(f, order='big', decode=False):
    big_little = {'little':'<', 'big':'>'}
    if decode:
        return f.read(1).decode()
    else:
        return struct.unpack(big_little[order] + 'B', f.read(1))[0]


def read16(f, order='big', decode=False):
    big_little = {'little':'<', 'big':'>'}
    if decode:
        return f.read(2).decode()
    else:
        return struct.unpack(big_little[order] + 'H', f.read(2))[0]


def read32(f, order='big', decode=False):
    big_little = {'little':'<', 'big':'>'}
    if decode:
        return f.read(4).decode()
    else:
        return struct.unpack(big_little[order] + 'L', f.read(4))[0]


def readn(f, size, order='big', decode=False):
    if size == 32:
        data = read32(f, order, decode)
    elif size == 16:
        data = read16(f, order, decode)
    elif size == 8:
        data = read8(f, order, decode)
    else:
        raise ValueError()

    return data


def read_null_terminated(f):
    NULL = b'\x00'
    SPACE = b'\x20'
    s = ''
    while True:
        c = read8(f, 'big', decode=True)
        s += c
        if c.encode() == NULL or c.encode() == SPACE:
            break
    return s

# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
