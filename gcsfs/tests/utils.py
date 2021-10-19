import subprocess
from contextlib import contextmanager
import gzip
import json
import os
import shlex
import shutil
import re
import pickle
import tempfile

import pytest

from gcsfs.core import GCSFileSystem


@contextmanager
def ignoring(*exceptions):
    try:
        yield
    except exceptions:
        pass


@contextmanager
def tempdir(dir=None):
    dirname = tempfile.mkdtemp(dir=dir)
    shutil.rmtree(dirname, ignore_errors=True)

    try:
        yield dirname
    finally:
        if os.path.exists(dirname):
            shutil.rmtree(dirname, ignore_errors=True)


@contextmanager
def tmpfile(extension="", dir=None):
    extension = "." + extension.lstrip(".")
    handle, filename = tempfile.mkstemp(extension, dir=dir)
    os.close(handle)
    os.remove(filename)

    try:
        yield filename
    finally:
        if os.path.exists(filename):
            if os.path.isdir(filename):
                shutil.rmtree(filename)
            else:
                with ignoring(OSError):
                    os.remove(filename)
