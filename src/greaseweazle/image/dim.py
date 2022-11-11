# greaseweazle/image/img.py
#
# Written & released by Keir Fraser <keir.xen@gmail.com>
#
# This is free and unencumbered software released into the public domain.
# See the file COPYING for more details, or visit <http://unlicense.org>.

import struct

from greaseweazle import error
from greaseweazle.image.img import IMG
from .image import Image

from greaseweazle.codec import formats

class DIM(IMG):
    default_format = 'pc98.hd'

    sides_swapped = False

    @classmethod
    def from_file(cls, name, fmt):

        with open(name, "rb") as f:
            header = f.read(256)
            error.check(header[0xAB:0xB8] == b"DIFC HEADER  ", "DIM: Not a DIM file.")
            (media_byte,) = struct.unpack('B255x', header)
            error.check(media_byte == 0, "DIM: Unsupported format.")
            dat = f.read()

        img = cls(name, fmt)

        pos = 0
        for t in fmt.max_tracks:
            cyl, head = t.cyl, t.head
            if img.sides_swapped:
                head ^= 1
            track = fmt.fmt(cyl, head)
            pos += track.set_img_track(dat[pos:])
            img.to_track[cyl,head] = track

        return img


    @classmethod
    def to_file(cls, name, fmt, noclobber):
        raise error.Fatal("DIM: Writing not supported.")

# Local variables:
# python-indent: 4
# End: