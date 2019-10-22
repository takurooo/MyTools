# -----------------------------------
# import
# -----------------------------------
import os
from collections import OrderedDict

from common.exif_defines import TagType, TAG_TYPE_SIZE, TAG_TYPE_NAME, TAG_NAME, GPS_TAG_NAME
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
class TiffHeader:
    BYTEORDER_BIG = 0x4d4d
    BYTEORDER_LITTLE = 0x4949
    CODE = 0x2a
    start_pos = None
    byteorder = None
    code = None
    ifd_offset = None
    ifd_pos = None


class Tag:
    id = None
    name = None
    start_pos = None
    type = None
    typesize = None
    typename = None
    num = None
    val = None


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
        tiff_header = TiffHeader()

        while self.remain_size() >= 4:
            byteorder = self.read_16bits()

            if byteorder == TiffHeader.BYTEORDER_LITTLE:
                tiff_header.byteorder = 'little'
                break
            elif byteorder == TiffHeader.BYTEORDER_BIG:
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

            # --------------------------------
            # parse ifd
            # --------------------------------
            self.seek(next_ifd_pos, whence=0)
            ifd, next_ifd_pos = self._read_ifd(TAG_NAME)

            # --------------------------------
            # parse ifd for Exif
            # --------------------------------
            ifd_exif = OrderedDict()
            exif_tag = ifd.get('ExifOffset', None)
            if exif_tag is not None:
                exif_ifd_pos = self.tiff_header.start_pos + exif_tag.val
                self.seek(exif_ifd_pos, whence=0)
                ifd_exif, _ = self._read_ifd(TAG_NAME)

            # --------------------------------
            # parse ifd for GPS
            # --------------------------------
            ifd_gps = OrderedDict()
            gps_tag = ifd.get('GPSInfo', None)
            if gps_tag is not None:
                gps_ifd_pos = self.tiff_header.start_pos + gps_tag.val
                self.seek(gps_ifd_pos, whence=0)
                ifd_gps, _ = self._read_ifd(GPS_TAG_NAME)

            ifd.update(ifd_exif)
            ifd.update(ifd_gps)
            ifds.append(ifd)

        return ifds

    def _read_ifd(self, tag_name_dic):
        ifd = OrderedDict()
        tag_num = self.read_16bits(byteorder=self.tiff_header.byteorder)
        for _ in range(tag_num):
            # --------------------------------
            # parse tag
            # --------------------------------
            tag = self._read_tag(tag_name_dic)
            ifd[tag.name] = tag

        # --------------------------------
        # tagの終端に次のifdへのオフセットがある.
        # オフセットが0の場合は次のifdがない.
        # --------------------------------
        next_ifd_offset = self.read_16bits(byteorder=self.tiff_header.byteorder)
        if next_ifd_offset != 0:
            next_ifd_pos = self.tiff_header.start_pos + next_ifd_offset
        else:
            next_ifd_pos = 0

        return ifd, next_ifd_pos

    def _read_tag(self, tag_name_dic):
        tag = Tag()

        tag.id = self.read_16bits(byteorder=self.tiff_header.byteorder)
        tag.type = self.read_16bits(byteorder=self.tiff_header.byteorder)
        tag.cnt = self.read_32bits(byteorder=self.tiff_header.byteorder)

        tag.start_pos = self.tell()
        val_or_offset = self.read_32bits(byteorder=self.tiff_header.byteorder)
        next_tag_pos = self.tell()

        tag.name = tag_name_dic.get(tag.id, tag.id)
        tag.typesize = TAG_TYPE_SIZE.get(tag.type, None)
        assert tag.typesize != None, 'tag type invalid {}, start pos {}'.format(tag.type,tag.start_pos)

        tag.typename = TAG_TYPE_NAME.get(tag.type, tag.type)
        total_size_bytes = tag.typesize * tag.cnt

        # ----------------------------------------------------------------
        # データの合計サイズが4バイトを超えている  -> val_or_offsetはデータへのオフセット
        # データの合計サイズが4バイトを超えていない -> val_or_offsetはデータ
        # ----------------------------------------------------------------
        if total_size_bytes <= 4:
            tag.val = val_or_offset
            if tag.name in BYTES_TYPE_TGAS:
                # PILの_getexif()とデータの形式を合わせる.
                tag.val = tag.val.to_bytes(total_size_bytes, byteorder=self.tiff_header.byteorder)
        else:
            tag.start_pos = self.tiff_header.start_pos + val_or_offset
            self.seek(tag.start_pos, whence=0)

            if tag.type == TagType.ASCII:
                tag.val = self.read_null_terminated()
                tag.val = tag.val[:-1]  # delete null
            elif tag.type == TagType.RATIONAL or tag.type == TagType.SRATIONAL:
                is_signed = tag.type == TagType.SRATIONAL
                size_bits = tag.typesize // 2 * 8
                tag.val = []
                for _ in range(tag.cnt):
                    numerator = self.read_nbits(size_bits, byteorder=self.tiff_header.byteorder, signed=is_signed)
                    denominator = self.read_nbits(size_bits, byteorder=self.tiff_header.byteorder, signed=is_signed)
                    tag.val.append((numerator, denominator))
            else:
                if tag.name in BYTES_TYPE_TGAS:
                    # PILの_getexif()とデータの形式を合わせる.
                    tag.val = self.read_raw(total_size_bytes)
                else:
                    tag.val = []
                    size_bits = tag.typesize * 8
                    for _ in range(tag.cnt):
                        tag.val.append(self.read_nbits(size_bits, byteorder=self.tiff_header.byteorder))

        # PILの_getexif()とデータの形式を合わせる.
        if isinstance(tag.val, list):
            if len(tag.val) == 1:
                tag.val = tag.val[0]
            else:
                tag.val = tuple(tag.val)

        self.add_log_for_html(tag)
        self.add_log('({:#06x}){:<30}  fpos: {:#06x}  typesize: {:>}({:>9})  valnum: {:<6}  val: {}'.format(
            tag.id, tag.name, tag.start_pos,
            tag.typesize, tag.typename,
            tag.cnt, tag.val)
        )

        self.seek(next_tag_pos, whence=0)

        return tag

    def get_exif(self):
        return self.ifds

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
            Cell(htmlwriter.TYPE_LINK, text='Exif Specification', link='http://www.cipa.jp/std/documents/j/DC-008-2012_J.pdf'),
            Cell(htmlwriter.TYPE_LINK, text='{}'.format(self.file_path), link=self.file_path),
            Cell(htmlwriter.TYPE_TEXT, text='ByteOrder : {}'.format(str(self.tiff_header.byteorder).upper()))
        ])

        writer.add_row([
            Cell(htmlwriter.TYPE_TEXT, text='tag id'),
            Cell(htmlwriter.TYPE_TEXT, text='tag name'),
            Cell(htmlwriter.TYPE_TEXT, text='file pos'),
            Cell(htmlwriter.TYPE_TEXT, text='val type'),
            Cell(htmlwriter.TYPE_TEXT, text='val cnt'),
            Cell(htmlwriter.TYPE_TEXT, text='val')
        ])

        DISPLAY_MAX_LEN = 50
        for tag in self.log_for_html:
            val = tag.val
            if len(str(tag.val)) > DISPLAY_MAX_LEN:
                val = '-- NOT DISPLAY --'

            writer.add_row([
                Cell(htmlwriter.TYPE_TEXT, text='{:#06x}'.format(tag.id)),
                Cell(htmlwriter.TYPE_TEXT, text=str(tag.name)),
                Cell(htmlwriter.TYPE_TEXT, text='{:#06x}'.format(tag.start_pos)),
                Cell(htmlwriter.TYPE_TEXT, text='{}({})'.format(tag.typesize,tag.typename)),
                Cell(htmlwriter.TYPE_TEXT, text=str(tag.cnt)),
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
