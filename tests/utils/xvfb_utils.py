"""This module implements utility functions for management of xvfb."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os
import time
import errno
import fnmatch
import tempfile
import subprocess as sp
from itertools import chain


def start_session(display, screens, screen_width, screen_height, screen_depth):
    whd = '{width}x{height}x{depth}'.format(width=screen_width,
                                            height=screen_height,
                                            depth=screen_depth)
    cmd = ['Xvfb', '-br', '-nolisten', 'tcp', ':{}'.format(display)]
    for screen in screens:
        cmd.extend(['-screen', str(screen), whd])

    with open(os.devnull, 'w') as dev_null:
        proc = sp.Popen(cmd, stdout=dev_null, stderr=dev_null, close_fds=True)

    # let Xvfb start
    time.sleep(0.5)
    if proc.poll() is not None:
        raise RuntimeError('Xvfb did not start')

    return proc


def stop_session(proc):
    try:
        proc.terminate()
        proc.wait()
    except IOError as ex:
        if ex.errno not in (errno.EINVAL, errno.EPIPE):
            raise


def find_free_display(min_display_num=1005):
    tmp_dir = tempfile.gettempdir()
    lock_files = fnmatch.filter(os.listdir(tmp_dir), '.X*-lock')
    displays_in_use = (int(name.split('X')[1].split('-')[0])
                       for name in lock_files
                       if os.path.isfile(os.path.join(tmp_dir, name)))
    return max(chain([min_display_num], displays_in_use)) + 1
