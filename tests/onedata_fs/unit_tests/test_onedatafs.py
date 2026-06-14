"""Unit tests executed inside an environment-provided oneclient container."""

import math
import random
import string
import time
import unittest
from datetime import datetime
from typing import ClassVar, cast

import pytz  # type: ignore[import-untyped]  # pylint: disable=import-error
import xmlrunner  # pylint: disable=import-error
import yaml
from fs.onedatafs import OnedataFS  # pylint: disable=import-error
from fs.test import FSTestCases  # pylint: disable=import-error

from . import (
    ACCESS_TOKEN,
    CONTAINER_REPORTS_XML_DIR,
    CONTAINER_TEST_CFG_FILE,
    PROVIDER_IP,
    SPACE_NAME,
)


class TestOnedataFS(FSTestCases, unittest.TestCase):
    provider_ip: ClassVar[str]
    token: ClassVar[str]
    space: ClassVar[str]
    odfs: ClassVar[OnedataFS]

    @classmethod
    def setUpClass(cls) -> None:
        with open(CONTAINER_TEST_CFG_FILE, "r") as f:
            cfg = cast(dict[str, str], yaml.load(f.read(), Loader=yaml.Loader))
            cls.provider_ip = cfg[PROVIDER_IP]
            cls.token = str(cfg[ACCESS_TOKEN])
            cls.space = cfg[SPACE_NAME]
        cls.odfs = OnedataFS(
            cls.provider_ip,
            cls.token,
            insecure=True,
            force_proxy_io=True,
            no_buffer=False,
            provider_timeout=120,
        ).opendir("/" + cls.space)

    @classmethod
    def tearDownClass(cls) -> None:
        time.sleep(5)
        # sometimes destroying OnedataFS throws Segmentation Fault
        # when it hadn't handled all requests
        try:
            cls.odfs.close()
        except:  # pylint: disable=bare-except
            pass

    def make_fs(self) -> OnedataFS:
        testdir = "".join(random.choice(string.ascii_lowercase) for _ in range(16))
        self.odfs.makedir(testdir)
        return self.odfs.opendir(testdir)

    def destroy_fs(self, fs: OnedataFS) -> None:
        pass

    def test_openbin_truncate(self) -> None:
        self.fs.writetext("foo", "abcd")
        self.fs.openbin("foo", "w").close()
        self.assertEqual(self.fs.getsize("foo"), 0)

    def test_setinfo_size(self) -> None:
        self.fs.writetext("foo", "abcd")
        self.fs.setinfo("foo", {"details": {"size": 1}})
        self.assertEqual(self.fs.getsize("foo"), 1)

    def test_setinfo_atime(self) -> None:
        self.fs.writetext("foo", "abcd")
        now = int(math.floor(time.time())) + 3600
        now_datetime = datetime.utcfromtimestamp(now).replace(tzinfo=pytz.UTC)
        self.fs.setinfo("foo", {"details": {"accessed": now}})
        self.assertEqual(
            self.fs.getinfo("foo", namespaces=["details"]).accessed, now_datetime
        )

    def test_setinfo_mtime(self) -> None:
        self.fs.writetext("foo", "abcd")
        now = int(math.floor(time.time()) + 3600)
        now_datetime = datetime.utcfromtimestamp(now).replace(tzinfo=pytz.UTC)
        self.fs.setinfo("foo", {"details": {"modified": now}})
        self.assertEqual(
            self.fs.getinfo("foo", namespaces=["details"]).modified, now_datetime
        )

    def test_setinfo_mode(self) -> None:
        self.fs.writetext("foo", "abcd")
        self.fs.setinfo(
            "foo", {"access": {"permissions": ["g_r", "o_x", "u_r", "u_w"]}}
        )
        self.assertEqual(
            self.fs.getinfo("foo", namespaces=["access"]).permissions.as_str(),
            "rw-r----x",
        )


if __name__ == "__main__":
    test_runner = xmlrunner.XMLTestRunner(output=CONTAINER_REPORTS_XML_DIR)
    unittest.main(testRunner=test_runner, verbosity=2)
