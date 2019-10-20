# -----------------------------------
# import
# -----------------------------------
import os
from collections import OrderedDict

from common.exif_defines import TagType, TAG_NAME, GPS_TAG_NAME
from common.binary_reader import BinaryReader
import common.htmlwriter as htmlwriter
from common.htmlwriter import HtmlTableWriter, Cell

# -----------------------------------
# define
# -----------------------------------

# bytes formatとして出力するtag PILと合わせている.
BYTES_TYPE_TGAS = [
    'PrintImageMatching',
    'MakerNote',
    'UserComment',
    'ExifVersion',
    'ComponentsConfiguration',
    'FlashPixVersion',
    'FileSource',
    'SceneType'
]


# -----------------------------------
# class
# -----------------------------------
def type2size(type):
    tagtype = {TagType.BYTE: 1,
               TagType.ASCII: 1,
               TagType.SHORT: 2,
               TagType.LONG: 4,
               TagType.RATIONAL: 8,
               TagType.UNDEFINED: 1,
               TagType.SLONG: 4,
               TagType.SRATIONAL: 8}

    return tagtype.get(type, None)


class TiffHeader:
    ORDER_BIG = 0x4d4d
    ORDER_LITTLE = 0x4949
    CODE = 0x2a
    start_pos = None
    byteorder = None
    code = None
    ifd_offset = None
    ifd_pos = None


class ExifReader(BinaryReader):
    def __init__(self, file_path):
        super(ExifReader, self).__init__(file_path)

        self.tiff_header = self._find_tiff_header()
        if self.tiff_header is None:
            raise ValueError('tiff header not found :', file_path)

        self.log_for_html = []
        self.add_log_for_html = self.log_for_html.append

        self.log = []
        self.add_log = self.log.append
        self.add_log('======================================')
        self.add_log('tiff header')
        self.add_log('======================================')
        self.add_log('tiff header pos : {:#04x}'.format(self.tiff_header.start_pos))
        self.add_log('ifd pos         : {:#04x}'.format(self.tiff_header.ifd_pos))
        self.add_log('endian          : {}'.format(self.tiff_header.byteorder))

        self.ifds = self._read_ifds()

        # print(self.ifds[0]['XResolution'])

    def _find_tiff_header(self):
        tiff_header = TiffHeader

        while self.remain_size() >= 2:
            v = self.read_16bits()

            if v == tiff_header.ORDER_LITTLE:
                tiff_header.byteorder = 'little'
                break

            if v == tiff_header.ORDER_BIG:
                tiff_header.byteorder = 'big'
                break

            self.seek(-1, whence=1)
        else:
            return None

        tiff_header.start_pos = self.tell() - 2
        tiff_header.code = self.read_16bits(byteorder=tiff_header.byteorder)

        if tiff_header.code != tiff_header.CODE:
            return None

        tiff_header.ifd_offset = self.read_32bits(byteorder=tiff_header.byteorder)
        tiff_header.ifd_pos = tiff_header.start_pos + tiff_header.ifd_offset

        return tiff_header

    def _read_ifds(self):
        ifds = []
        next_ifd_pos = self.tiff_header.ifd_pos
        while next_ifd_pos != 0:
            self.add_log('')
            self.add_log('======================================')
            self.add_log('ifd : {}'.format(len(ifds)))
            self.add_log('pos : {:#04x}'.format(next_ifd_pos))
            self.add_log('======================================')

            self.seek(next_ifd_pos, whence=0)
            ifd, next_ifd_pos = self._read_ifd(TAG_NAME)

            _exif = OrderedDict()
            exif_ifd_offset = ifd.get('ExifOffset', None)
            if exif_ifd_offset:
                exif_ifd_pos = self.tiff_header.start_pos + exif_ifd_offset
                self.seek(exif_ifd_pos, whence=0)
                _exif, _ = self._read_ifd(TAG_NAME)

            _gps = OrderedDict()
            gps_ifd_offset = ifd.get('GPSInfo', None)
            if gps_ifd_offset:
                gps_ifd_pos = self.tiff_header.start_pos + gps_ifd_offset
                self.seek(gps_ifd_pos, whence=0)
                _gps, _ = self._read_ifd(GPS_TAG_NAME)

            ifd.update(_exif)
            ifd.update(_gps)
            ifds.append(ifd)

        return ifds

    def _read_ifd(self, tag_name_dic):
        ifd = OrderedDict()
        tag_num = self.read_16bits(byteorder=self.tiff_header.byteorder)
        for _ in range(tag_num):
            tag_name, val = self._read_tag(tag_name_dic)
            ifd[tag_name] = val

        next_ifd_offset = self.read_16bits(byteorder=self.tiff_header.byteorder)
        if next_ifd_offset != 0:
            next_ifd_pos = self.tiff_header.start_pos + next_ifd_offset
        else:
            next_ifd_pos = 0

        return ifd, next_ifd_pos

    def _read_tag(self, tag_name_dic):
        tag_id = self.read_16bits(byteorder=self.tiff_header.byteorder)
        tag_type = self.read_16bits(byteorder=self.tiff_header.byteorder)
        val_num = self.read_32bits(byteorder=self.tiff_header.byteorder)
        val_pos = self.tell()
        val_or_offset = self.read_32bits(byteorder=self.tiff_header.byteorder)
        next_tag_pos = self.tell()

        tag_name = tag_name_dic.get(tag_id, tag_id)
        type_size_bytes = type2size(tag_type)

        total_size_bytes = type_size_bytes * val_num

        if total_size_bytes <= 4:
            val = val_or_offset
            if tag_name in BYTES_TYPE_TGAS:
                # PILの_getexif()とデータの形式を合わせる.
                val = val.to_bytes(total_size_bytes, byteorder=self.tiff_header.byteorder)
        else:
            val_pos = self.tiff_header.start_pos + val_or_offset
            self.seek(val_pos, whence=0)

            if tag_type == TagType.ASCII:
                val = self.read_null_terminated()
                val = val[:-1]  # delete null
            elif tag_type == TagType.RATIONAL or tag_type == TagType.SRATIONAL:
                is_signed = tag_type == TagType.SRATIONAL
                size_bits = type_size_bytes // 2 * 8
                val = []
                for _ in range(val_num):
                    numerator = self.read_nbits(size_bits, byteorder=self.tiff_header.byteorder, signed=is_signed)
                    denominator = self.read_nbits(size_bits, byteorder=self.tiff_header.byteorder, signed=is_signed)
                    val.append((numerator, denominator))
            else:
                if tag_name in BYTES_TYPE_TGAS:
                    # PILの_getexif()とデータの形式を合わせる.
                    val = self.read_raw(total_size_bytes)
                else:
                    val = []
                    size_bits = type_size_bytes * 8
                    for _ in range(val_num):
                        val.append(self.read_nbits(size_bits, byteorder=self.tiff_header.byteorder))

        # PILの_getexif()とデータの形式を合わせる.
        if isinstance(val, list):
            if len(val) == 1:
                val = val[0]
            else:
                val = tuple(val)

        self.add_log('({:#06x}){:<30} val_pos: {:#06x}  valsize: {:<2}  valnum: {:<6}  val: {}'.format(
            tag_id, tag_name,
            val_pos,
            type_size_bytes,
            val_num,
            val)
        )

        self.add_log_for_html([
            tag_id,
            tag_name,
            val_pos,
            type_size_bytes,
            val_num,
            val]
        )

        self.seek(next_tag_pos, whence=0)

        return tag_name, val

    def print_log(self):
        print('\n'.join(self.log))

    def save_log(self, fname):
        _, ext = os.path.splitext(fname)
        if ext == '.html':
            self.save_as_html(fname)
        else:
            # save as text
            with open(fname, 'w') as f:
                for line in self.log:
                    f.write(line + '\n')

    def save_as_html(self, fname):
        CSS_FNAME = "style/sample.css"
        writer = HtmlTableWriter(fname,
                                 title='Exif Viewer',
                                 header='Exif Viewer',
                                 css_fname=CSS_FNAME)

        writer.add_summary([
            Cell(htmlwriter.TYPE_TEXT, text='Input file : {}'.format(self.file_path)),
            Cell(htmlwriter.TYPE_TEXT, text='Endian     : {}'.format(self.tiff_header.byteorder))
        ])

        writer.add_row([
            Cell(htmlwriter.TYPE_TEXT, text='tag id'),
            Cell(htmlwriter.TYPE_TEXT, text='tag name'),
            Cell(htmlwriter.TYPE_TEXT, text='file pos'),
            Cell(htmlwriter.TYPE_TEXT, text='val size'),
            Cell(htmlwriter.TYPE_TEXT, text='val num'),
            Cell(htmlwriter.TYPE_TEXT, text='val')
        ])

        DISPLAY_MAX_LEN = 50
        for line in self.log_for_html:
            tag_id, tag_name, pos, size, num, val = line

            if len(str(val)) > DISPLAY_MAX_LEN:
                val = '-- NOT DISPLAY --'

            writer.add_row([
                Cell(htmlwriter.TYPE_TEXT, text='{:#06x}'.format(tag_id)),
                Cell(htmlwriter.TYPE_TEXT, text=str(tag_name)),
                Cell(htmlwriter.TYPE_TEXT, text='{:#06x}'.format(pos)),
                Cell(htmlwriter.TYPE_TEXT, text=str(size)),
                Cell(htmlwriter.TYPE_TEXT, text=str(num)),
                Cell(htmlwriter.TYPE_TEXT, text=str(val))
            ])

        writer.write()


# -----------------------------------
# function
# -----------------------------------


# -----------------------------------
# main
# -----------------------------------

if __name__ == '__main__':
    pass
