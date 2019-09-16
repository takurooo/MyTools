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
class MetaBox(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘meta’
    Container: File, Movie Box (‘moov’), or Track Box (‘trak’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self, f):
        super(MetaBox, self).__init__()
        # HandlerBox(handler_type) theHandler;
        # PrimaryItemBox primary_resource; // optional
        # DataInformationBox file_locations; // optional
        # ItemLocationBox item_locations; // optional
        # ItemProtectionBox protections; // optional
        # ItemInfoBox item_infos; // optional
        # IPMPControlBox IPMP_control; // optional
        # Box other_boxes[]; // optional


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass