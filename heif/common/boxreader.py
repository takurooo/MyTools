# -----------------------------------
# import
# -----------------------------------
import os
from collections import OrderedDict

from common.basebox import Box, FullBox
from common.ftypebox import FileTypeBox
from common.metabox import MetaBox
from common.hdlrbox import HandlerReferenceBox
from common.ilocbox import ItemLocationBox
from common.iinfbox import ItemInformationBox
from common.pitmbox import PrimaryItemBox
from common.mdatbox import MediaDataBox
from common.iprpbox import ItemPropertiesBox
from common.irefbox import ItemReferenceBox

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
class BoxInfoDeployer:
    """
    BoxInfoDeployer for HEIF
    """

    def __init__(self):
        self._boxinfo = {
            'ftyp':{'child':False, 'fullbox':False, 'class':FileTypeBox},
            'meta':{'child':True, 'fullbox':True, 'class':MetaBox},
            'hdlr':{'child':False, 'fullbox':True, 'class':HandlerReferenceBox},
            'iloc':{'child':False, 'fullbox':True, 'class':ItemLocationBox},
            'iinf':{'child':False, 'fullbox':True, 'class':ItemInformationBox},
            'pitm':{'child':False, 'fullbox':True, 'class':PrimaryItemBox},
            'iprp':{'child':False, 'fullbox':False, 'class':ItemPropertiesBox},
            'iref':{'child':False, 'fullbox':True, 'class':ItemReferenceBox},
            'mdat':{'child':False, 'fullbox':False, 'class':MediaDataBox},
        }

    def has_child(self, boxtype):
        target_box_info = self._boxinfo.get(boxtype, None)
        if target_box_info is not None:
            return target_box_info['child']
        else:
            return False

    def is_fullbox(self, boxtype):
        target_box_info = self._boxinfo.get(boxtype, None)
        if target_box_info is not None:
            return target_box_info['fullbox']
        else:
            return False

    def get_box_class(self, boxtype):
        target_box_info = self._boxinfo.get(boxtype, None)
        if target_box_info is not None:
            return target_box_info.get('class', None)
        else:
            return None


class BoxReader:
    """
    Box reader
    """

    def __init__(self, path):
        self.file_size = os.path.getsize(path)
        self.f = open(path, 'rb')
        self.box_pos = OrderedDict()
        self.boxinfo_deployer = BoxInfoDeployer()

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
        self.box_pos[box.type] = {'size':box.size, 'fp':box.start_fp}
        data_size = box.size - BOX_HEADER_SIZE

        if self._has_child(box.type):

            children_size = data_size
            if self._is_fullbox(box.type):
                # FullBox: unsigned int(8) version; bit(24) flags;
                fullbox_info_size = 4
                f.seek(fullbox_info_size, 1)  # f.seek(offset, whence)
                children_size -= fullbox_info_size

            while 0 < children_size:
                child_size = self._read_box(f)
                children_size -= child_size

        else:
            f.seek(data_size, 1)

        return box.size

    def _has_child(self, boxtype):
        return self.boxinfo_deployer.has_child(boxtype)

    def _is_fullbox(self, boxtype):
        return self.boxinfo_deployer.is_fullbox(boxtype)

    def _get_box_class(self, boxtype):
        return self.boxinfo_deployer.get_box_class(boxtype)

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
