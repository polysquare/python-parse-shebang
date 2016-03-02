# /test/test_acceptance.py
#
# Acceptance tests for the parseshebang module
#
# See /LICENCE.md for Copyright information
"""Acceptance tests for the parseshebang module."""

import os

import shutil

import stat

import subprocess

from tempfile import mkdtemp

from parseshebang import parse

from testtools import TestCase


class TestAcceptance(TestCase):
    """Acceptance tests for parseshebang."""

    def setUp(self):
        """Clear PATHEXT."""
        super(TestAcceptance, self).setUp()
        self.addCleanup(os.environ.update,
                        dict(PATHEXT=os.environ.get("PATHEXT", "")))
        os.environ.pop("PATHEXT", None)

    def test_popen_script(self):
        """Run a python script with subprocess.check_call."""
        script = ("#!/usr/bin/env python\n"
                  "import sys\n"
                  "sys.exit(0)\n")
        tempdir = mkdtemp(dir=os.getcwd(), prefix="parseshebang_acceptance")
        self.addCleanup(shutil.rmtree, tempdir)
        with open(os.path.join(tempdir, "script.py"), "w") as script_file:
            script_file.write(script)

        os.chmod(script_file.name,
                 os.stat(script_file.name).st_mode |
                 stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        shebang = parse(script_file.name)
        self.assertEqual(subprocess.check_call(shebang + [script_file.name]),
                         0)
