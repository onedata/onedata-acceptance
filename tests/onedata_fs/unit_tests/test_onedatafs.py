import unittest
import random
import string
import time
import math
import pytz
from datetime import datetime

import xmlrunner
import yaml

from fs.onedatafs import OnedataFS
from fs.test import FSTestCases
from . import (CONTAINER_REPORTS_XML_DIR, CONTAINER_TEST_CFG_FILE,
               ACCESS_TOKEN, SPACE_NAME, PROVIDER_IP)


class TestOnedataFS(FSTestCases, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(CONTAINER_TEST_CFG_FILE, 'r') as f:
            cfg = yaml.load(f.read(), Loader=yaml.Loader)
            cls.provider_ip = cfg[PROVIDER_IP]
            cls.token = str(cfg[ACCESS_TOKEN])
            cls.space = cfg[SPACE_NAME]

    def make_fs(self):
        odfs = OnedataFS(self.provider_ip, self.token, insecure=True,
                         force_proxy_io=True, no_buffer=False).opendir(
            '/' + self.space)
        testdir = ''.join(
            random.choice(string.ascii_lowercase) for _ in range(16))
        odfs.makedir(testdir)
        return odfs.opendir(testdir)

    def destroy_fs(self, fs):
        time.sleep(4)
        # sometimes destroying OnedataFS throws Segmentation Fault when
        try:
            fs.close()
        except:
            pass

    def test_openbin_truncate(self):
        self.fs.writetext('foo', u'abcd')
        self.fs.openbin('foo', 'w').close()
        self.assertEqual(self.fs.getsize('foo'), 0)

    def test_setinfo_size(self):
        self.fs.writetext('foo', u'abcd')
        self.fs.setinfo('foo', {'details': {'size': 1}})
        self.assertEqual(self.fs.getsize('foo'), 1)

    def test_setinfo_atime(self):
        self.fs.writetext('foo', u'abcd')
        now = int(math.floor(time.time())) + 3600
        now_datetime = datetime.utcfromtimestamp(now).replace(tzinfo=pytz.UTC)
        self.fs.setinfo('foo', {'details': {'accessed': now}})
        self.assertEqual(
            self.fs.getinfo('foo', namespaces=['details']).accessed,
            now_datetime)

    def test_setinfo_mtime(self):
        self.fs.writetext('foo', u'abcd')
        now = int(math.floor(time.time()) + 3600)
        now_datetime = datetime.utcfromtimestamp(now).replace(tzinfo=pytz.UTC)
        self.fs.setinfo('foo', {'details': {'modified': now}})
        self.assertEqual(
            self.fs.getinfo('foo', namespaces=['details']).modified,
            now_datetime)

    def test_setinfo_mode(self):
        self.fs.writetext('foo', u'abcd')
        self.fs.setinfo('foo', {'access': {'permissions': [u'g_r', u'o_x', u'u_r', u'u_w']}})
        self.assertEqual(self.fs.getinfo('foo', namespaces=['access']).permissions.as_str(), u'rw-r----x')


if __name__ == '__main__':
    test_runner = xmlrunner.XMLTestRunner(output=CONTAINER_REPORTS_XML_DIR)
    unittest.main(testRunner=test_runner, verbosity=2)
