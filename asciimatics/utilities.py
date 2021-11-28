
"""
This module is just a collection of simple helper functions.
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from datetime import date, datetime
from logging import getLogger

from asciimatics.constants import ASCII_LINE, SINGLE_LINE, DOUBLE_LINE


# Diagnostic logging
logger = getLogger(__name__)


def readable_mem(mem):
    """
    :param mem: An integer number of bytes to convert to human-readable form.
    :return: A human-readable string representation of the number.
    """
    for suffix in ["", "K", "M", "G", "T"]:
        if mem < 10000:
            return "{}{}".format(int(mem), suffix)
        mem /= 1024
    return "{}P".format(int(mem))


def readable_timestamp(stamp):
    """
    :param stamp: A floating point number representing the POSIX file timestamp.
    :return: A short human-readable string representation of the timestamp.
    """
    if date.fromtimestamp(stamp) == date.today():
        return str(datetime.fromtimestamp(stamp).strftime("%I:%M:%S%p"))
    else:
        return str(date.fromtimestamp(stamp))


class _DotDict(dict):
    """
    Modified dictionary to allow dot notation access.

    This can be used for quick and easy structures.  See https://stackoverflow.com/q/2352181/4994021
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class BoxTool:
    """Tool for building boxes out of characters. Supports a variety of line
    styles from `asciimatics.constants`:

    * ``ASCII_LINE`` -- ASCII safe characters (0)
    * ``SINGLE_LINE`` -- Unicode based single lined box (1)
    * ``DOUBLE_LINE`` -- Unicode based double lined box (2)

    Individual characters of a box can be accessed directly through attributes:

    * ``up_left`` -- corner piece facing up and left
    * ``up_right`` -- corner piece facing up and right
    * ``down_left`` -- corner piece facing down and left
    * ``down_right`` -- corner piece facing down and right
    * ``h`` -- horizontal line 
    * ``v`` --  vertical line 
    * ``v_inside`` --  vertical line used inside the grid
    * ``v_left`` -- vertical line with mid joiner facing to the left
    * ``v_right`` -- vertical line with mid joiner facing to the right
    * ``h_up`` -- horizontal line with a mid joiner facing up
    * ``h_down`` -- horizontal line with a mid joiner facing down
    * ``cross`` -- intersection between vertical and horizontal
    """
    def __init__(self, unicode_aware, style=SINGLE_LINE):
        """**Initialization:**

        :param unicode_aware: boolean indicating if the terminal is Unicode
            aware. If False, will force the use of the ASCII style
        :param style: line style specifier. Supports ``ASCII_LINE``,
            ``SINGLE_LINE``, and ``DOUBLE_LINE``. Defaults to ``SINGLE_LINE``.
        """
        self.unicode_aware = unicode_aware
        self.style = style

    @property
    def style(self):
        """The line drawing style used to draw boxes. Possible styles are set
        in :mod:`asciimatics.constants`.

        :param style: One of ``ASCII_LINE``, ``SINGLE_LINE``, or ``DOUBLE_LINE``
        """
        return self._style

    @style.setter
    def style(self, style):
        self._style = style

        if style == SINGLE_LINE and self.unicode_aware:
            self.down_right = u"┌"
            self.down_left = u"┐"
            self.up_right = u"└"
            self.up_left = u"┘"
            self.h = u"─"
            self.h_inside = u"─"
            self.v = u"│"
            self.v_inside = u"│"
            self.v_left = u"┤"
            self.v_right = u"├"
            self.h_up = u"┴"
            self.h_down = u"┬"
            self.cross = u"┼"
        elif style == DOUBLE_LINE and self.unicode_aware:
            self.down_right = u"╔"
            self.down_left = u"╗"
            self.up_right = u"╚"
            self.up_left = u"╝"
            self.h = u"═"
            self.h_inside = u"═"
            self.v = u"║"
            self.v_inside = u"║"
            self.v_left = u"╣"
            self.v_right = u"╠"
            self.h_up = u"╩"
            self.h_down = u"╦"
            self.cross = u"╬"
        else:
            self.down_left = "+"
            self.down_right = "+"
            self.up_right = u"+"
            self.up_left = u"+"
            self.h = "-"
            self.h_inside = "-"
            self.v = "|"
            self.v_inside = ":"
            self.v_left = "+"
            self.v_right = "+"
            self.h_up = u"+"
            self.h_down = "+"
            self.cross = "+"

    # --- Empty box methods
    def box_top(self, width):
        """Returns a string containing the top border of a box

        :param width: width of box, including corners
        """
        return self.down_right + (width - 2) * self.h + self.down_left

    def box_bottom(self, width):
        """Returns a string containing the bottom border of a box

        :param width: width of box, including corners
        """
        return self.up_right + (width - 2) * self.h + self.up_left

    def box_line(self, width):
        """Returns a string with a vertical bar on each end, padded with
        spaces in between for the given width.

        :param width: width of box including sides
        """
        return self.v + (width - 2) * ' ' + self.v

    def box(self, width, height):
        """Returns a string containing a box with the given width and
        height"""
        lines = [self.box_top(width)]
        for _ in range(height - 2):
            lines.append(self.box_line(width))

        lines.append(self.box_bottom(width))
        return '\n'.join(lines) + '\n'
