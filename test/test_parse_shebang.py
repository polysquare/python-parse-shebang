# /test/test_parse_shebang.py
#
# Unit tests for the parseshebang module
#
# See /LICENCE.md for Copyright information
"""Unit tests for the parseshebang module."""

import io

import os

import platform

import shutil

import struct

from tempfile import mkdtemp

from nose_parameterized import param, parameterized

from parseshebang import parse

from six import StringIO

from testtools import ExpectedException, TestCase


# suppress(too-few-public-methods)
class Function(object):
    """Wrapper for a function."""

    def __init__(self, func, description):
        """Store description and func."""
        super(Function, self).__init__()
        self._func = func
        self._description = description

    def __str__(self):
        """Return description."""
        return self._description

    def __call__(self, *args, **kwargs):
        """Forward function call to underlying func."""
        return self._func(*args, **kwargs)


def _from_fileobj(text, cleanup, **kwargs):
    """Return a StringIO with our text."""
    del cleanup
    del kwargs

    return StringIO(text)


def _from_filename(text, cleanup, mode="w", **kwargs):
    """Write a filename in a temporary directory."""
    del kwargs

    tempdir = mkdtemp(dir=os.getcwd(), prefix="parseshebang_unit")
    cleanup(shutil.rmtree, tempdir)
    with open(os.path.join(tempdir, "script.py"), mode) as script:
        script.write(text)

    return script.name


MODES = (param(Function(_from_fileobj, "from file object")),
         param(Function(_from_filename, "from file name")))


def _print_mode(func, num, params):
    """Format docstring for tests with extra flags if necessary."""
    del num

    return func.__doc__[:-1] + """ with input {}.""".format(str(params[0][0]))


class TestShebangParser(TestCase):
    """Unit test fixture for parse() function."""

    def setUp(self):
        """Clear PATHEXT."""
        super(TestShebangParser, self).setUp()
        self.addCleanup(os.environ.update,
                        dict(PATHEXT=os.environ.get("PATHEXT", "")))
        os.environ.pop("PATHEXT", None)

    @parameterized.expand(MODES, testcase_func_doc=_print_mode)
    def test_parse_single_part_shebang(self, mode):
        """Parse a single-part shebang."""
        self.assertEqual(parse(mode("#!python\n", self.addCleanup)),
                         ["python"])

    @parameterized.expand(MODES, testcase_func_doc=_print_mode)
    def test_parse_multi_part_shebang_linux(self, mode):
        """Parse a multi-part shebang, keeping env."""
        if platform.system() == "Windows":
            self.skipTest("""Keeping env only makes sense on POSIX.""")

        self.assertEqual(parse(mode("#!/usr/bin/env python\n",
                                    self.addCleanup)),
                         ["/usr/bin/env", "python"])

    @parameterized.expand(MODES, testcase_func_doc=_print_mode)
    def test_parse_multi_part_shebang_windows(self, mode):
        """Parse a multi-part shebang, discarding env."""
        if platform.system() != "Windows":
            self.skipTest("""Discarding env only makes sense on Windows.""")

        self.assertEqual(parse(mode("#!/usr/bin/env python\n",
                                    self.addCleanup)),
                         ["python"])

    @parameterized.expand(MODES, testcase_func_doc=_print_mode)
    def test_parse_multi_part_shebang_nonenv(self, mode):
        """Parse a multi-part shebang, keeping non-env."""
        self.assertEqual(parse(mode("#!/usr/bin/nonenv python\n",
                                    self.addCleanup)),
                         ["/usr/bin/nonenv", "python"])

    @parameterized.expand(MODES, testcase_func_doc=_print_mode)
    def test_parse_multi_part_shebang_extra_spaces(self, mode):
        """Parse a multi-part shebang, keeping non-env."""
        self.assertEqual(parse(mode("#!/usr/bin/nonenv    python\n",
                                    self.addCleanup)),
                         ["/usr/bin/nonenv", "python"])

    @parameterized.expand(MODES, testcase_func_doc=_print_mode)
    def test_parse_no_shebang(self, mode):
        """Parse no shebang."""
        self.assertEqual(parse(mode("", self.addCleanup)),
                         [])

    def test_parse_no_shebang_from_binary(self):
        """Handle binaries."""
        self.assertEqual(parse(_from_filename(struct.pack("2i",
                                                          *(99999, 99999)),
                                              self.addCleanup,
                                              mode="wb")),
                         [])

    def test_no_parse_shebang_if_in_pathext(self):
        """Don't parse shebang from file if extension is in PATHEXT."""
        os.environ["PATHEXT"] = ".py"
        self.assertEqual(parse(_from_filename("#!python",
                                              self.addCleanup)),
                         [])

    # suppress(no-self-use)
    def test_throw_runtime_error_when_weird_object_passed(self):
        """Raise RuntimeError when weird object is passed in."""
        with ExpectedException(RuntimeError):
            parse(object())

    # suppress(no-self-use)
    def test_unicode(self):
        """A filename can be text which in python 2 is not `str`."""
        tmpdir = mkdtemp()
        self.addCleanup(shutil.rmtree, tmpdir)

        filename = os.path.join(tmpdir, u"foo.sh")
        with io.open(filename, "w") as f:
            f.write(u"#!/usr/bin/python\n")

        self.assertEqual(parse(filename), ["/usr/bin/python"])

    # suppress(no-self-use)
    def test_filename_without_extension(self):
        """Regression test for no-PATHEXT no-extension."""
        tmpdir = mkdtemp()
        self.addCleanup(shutil.rmtree, tmpdir)

        filename = os.path.join(tmpdir, u"foo")
        with io.open(filename, "w") as f:
            f.write(u"#!/usr/bin/python\n")

        self.assertEqual(parse(filename), ["/usr/bin/python"])
