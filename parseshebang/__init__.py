# /parseshebang/__init__.py
#
# Provides a parse() method, where either a filename or file
# object can be passed in. The file is checked for a #! marker
# at the beginning and if it has it, a list of command line fragments
# will be returned.
#
# See /LICENCE.md for Copyright information
"""Main module for parseshebang."""

import os

import platform

import shlex

import six


def _parse(fileobj):
    """Parse fileobj for a shebang."""
    fileobj.seek(0)
    try:
        part = fileobj.read(2)
    except UnicodeDecodeError:
        part = ""

    if part == "#!":
        shebang = shlex.split(fileobj.readline().strip())
        if (platform.system() == "Windows" and
                len(shebang) and
                os.path.basename(shebang[0]) == "env"):
            return shebang[1:]

        return shebang

    return []


def parse(file_to_parse):  # suppress(unused-function)
    """Check file_to_parse for a shebang and return its components.

    :file_to_parse: can be either a filename or an open file object.

    If file_to_parse's extension exists in PATHEXT then an empty list
    will be returned, as it is assumed that the operating system knows
    how to handle files of this type. All other files will be opened
    and read.
    """
    if hasattr(file_to_parse, "read"):
        return _parse(file_to_parse)
    elif isinstance(file_to_parse, six.string_types):
        if "PATHEXT" in os.environ:
            path_ext = os.environ["PATHEXT"].split(os.pathsep)
        else:
            path_ext = ()
        if os.path.splitext(file_to_parse)[1] in path_ext:
            return []

        with open(file_to_parse, "r") as fileobj:
            return _parse(fileobj)

    raise RuntimeError("""{} was not a file-like """
                       """object.""".format(repr(file_to_parse)))
