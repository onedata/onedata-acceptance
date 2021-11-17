"""This module contains gherkin steps to run acceptance tests featuring
interacting with local file system.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import os
import pdb
import stat
import subprocess

import requests
import yaml

from tests.gui.utils.generic import suppress
from tests.utils.bdd_utils import given, parsers, wt
from tests.gui.conftest import WAIT_BACKEND
from tests.utils.utils import repeat_failed

PERMS_777 = stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH


@given(parsers.parse('directory tree structure on local '
                     'file system:\n{structure}'))
def create_dir_tree_structure_on_local_fs(structure, tmpdir):
    """Create directory tree structure on local storage.

    Directory tree structure format given in yaml is as follow:

    user_name:                ---> currently we identify user
                                   account with concrete
                                   browser so user_name == browser_id
        dir1: 5             ---> if item name startswith 'dir' it is
                                   considered directory otherwise a file;
                                   with given num, [num] files with random
                                   contest will be created
        dir2:
          dir21
            dir22:
              file1.txt:
                content: guana_bana_kunkwa_persi_mona_sala  ---> when
                                                            specifying file,
                                                            one can specify it's
                                                            content as well
                size: 5 MiB                ---> OR one can specify size
                                                (default in bytes unless
                                                specified otherwise)
                                               ---> SIZE OVERRIDES CONTENT
    """

    for user, home_dir_content in yaml.load(structure).items():
        home_dir = tmpdir.join(user)
        with suppress(OSError):
            home_dir.mkdir()
        _mkdirs(home_dir, home_dir_content)


def _mkdirs(cwd, dir_content=None):
    if not dir_content:
        return

    try:
        files_num = int(dir_content)
    except (TypeError, ValueError):
        for item in dir_content:
            if item.startswith('dir'):
                new_dir = cwd.join(item)
                new_dir.mkdir()
                new_dir.chmod(PERMS_777)
                _mkdirs(new_dir, dir_content[item])
            else:
                content = dir_content[item].get('content', None)
                size = dir_content[item].get('size', None)
                if size:
                    size = specify_size(size)
                    content = size * '1'

                _mkfile(cwd.join(item), content)
    else:
        for i in range(files_num):
            _mkfile(cwd.join('file{}.txt'.format(i)))


def specify_size(size_string):
    try:
        return int(size_string)
    except ValueError:
        unit_dict = {'B': 1, 'KiB': 1024, 'MiB': 1024 * 1024,
                     'GiB': 1024 * 1024 * 1024}
        [size, unit] = size_string.split()
        return int(size) * unit_dict[unit]


def _mkfile(file_, file_content=None):
    if not file_content:
        file_content = '1' * 10

    file_.write(file_content)
    file_.chmod(PERMS_777)


@given(parsers.parse('user of {browser_id} downloads {file_url} as '
                     '{file_name} to local file system'))
def download_file_to_local_file_system(browser_id, file_url, file_name,
                                       tmpdir):
    home_dir = tmpdir.join(browser_id)
    os.makedirs(home_dir, exist_ok=True)

    r = requests.get(file_url, allow_redirects=True)
    open(home_dir.join(file_name), 'wb').write(r.content)


@given(parsers.parse('user of {browser_id} creates file named "{file_name}" '
                     'sized: {item_size} in "{directory_name}" on local file '
                     'system'))
def create_file_on_local_file_system(browser_id, file_name, item_size,
                                     directory_name, tmpdir):
    home_dir = tmpdir.join(browser_id)
    path = home_dir + directory_name
    size = specify_size(item_size)
    content = size * '1'

    _mkfile(path.join(file_name), content)


@wt(parsers.parse('user of {browser_id} removes "{path}" from local file '
                  'system'))
@repeat_failed(timeout=WAIT_BACKEND)
def remove_file_from_local_file_system(browser_id, path, tmpdir):
    home_dir = tmpdir.join(browser_id)

    cmd = ['rm', home_dir + path]
    subprocess.check_call(cmd)
