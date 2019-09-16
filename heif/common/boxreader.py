# -----------------------------------
# import
# -----------------------------------
import os
from collections import OrderedDict

from common import futils
from common.basebox import Box, FullBox
from common.filetypebox import FileTypeBox
from common.metabox import MetaBox
from common.handlerreferencebox import HandlerReferenceBox
from common.itemlocationbox import ItemLocationBox
from common.iteminformationbox import ItemInformationBox
from common.primaryitembox import PrimaryItemBox

# -----------------------------------
# define
# -----------------------------------
BOX_HEADER_SIZE = 8

# -----------------------------------
# function
# -----------------------------------


# -----------------------------------
# class
# -----------------------------------
class BoxReader:
    box_info = {
        'ftyp':{'child':False, 'fullbox':False, 'class':FileTypeBox},
        'meta':{'child':True, 'fullbox':True, 'class':MetaBox},
        'hdlr':{'child':False, 'fullbox':True, 'class':HandlerReferenceBox},
        'iloc':{'child':False, 'fullbox':True, 'class':ItemLocationBox},
        'iinf':{'child':False, 'fullbox':True, 'class':ItemInformationBox},
        'pitm':{'child':False, 'fullbox':True, 'class':PrimaryItemBox},
        'iprp':{'child':True, 'fullbox':False},  # TODO
        'ipco':{'child':False, 'fullbox':False},  # TODO
        'ipma':{'child':False, 'fullbox':True},
        'dinf':{'child':True, 'fullbox':False},
        'dref':{'child':False, 'fullbox':True},
        'mdat':{'child':False, 'fullbox':False},
    }

    def __init__(self, path):
        self.file_size = os.path.getsize(path)
        self.f = open(path, 'rb')
        self.box_pos = OrderedDict()

    def __del__(self):
        self.f.close()

    def read_boxes(self):
        self.f.seek(0)

        total_file_size = self.file_size
        while 0 < total_file_size:
            boxsize = self._read_box(self.f)
            total_file_size -= boxsize

        return tuple(self.box_pos.keys())

    def _read_box(self, f):
        box = Box(f)

        self.box_pos[box.type] = {'size':box.size, 'fp':f.tell() - BOX_HEADER_SIZE}

        data_size = box.size - BOX_HEADER_SIZE

        if self._has_child(box.type):
            children_size = data_size

            if self._is_fullbox(box.type):
                futils.read32(f, 'big')  # TODO
                # FullBox
                # unsigned int(8) version = v;
                # bit(24) flags = f;
                children_size -= 4

            while 0 < children_size:
                child_size = self._read_box(f)
                children_size -= child_size

        else:
            f.read(data_size)

        return box.size

    def _has_child(self, boxtype):
        target_box_info = self.box_info.get(boxtype, None)
        if target_box_info is not None:
            return target_box_info['child']
        else:
            return False

    def _is_fullbox(self, boxtype):
        target_box_info = self.box_info.get(boxtype, None)
        if target_box_info is not None:
            return target_box_info['fullbox']
        else:
            return False

    def _get_box_class(self, boxtype):
        target_box_info = self.box_info.get(boxtype, None)
        if target_box_info is not None:
            return target_box_info.get('class', None)
        else:
            return None

    def get_box(self, boxtype):
        target_box_pos = self.box_pos.get(boxtype, None)

        if target_box_pos is None:
            return None

        target_box_class = self._get_box_class(boxtype)
        if target_box_class is not None:
            self.f.seek(target_box_pos['fp'])
            box = target_box_class(self.f)
            return box
        else:
            return None


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass