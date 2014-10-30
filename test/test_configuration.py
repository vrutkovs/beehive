from __future__ import with_statement
import unittest
import os.path
import tempfile

from nose.tools import eq_, ok_
from beehive import configuration

# one entry of each kind handled
TEST_CONFIG = '''[beehive]
outfiles= /absolute/path1
          relative/path2
paths = /absolute/path3
        relative/path4
tags = @foo,~@bar
       @zap
format=pretty
       tag-counter
stdout_capture=no
bogus=spam

[userdata]
foo = bar
'''


class TestConfiguration(object):

    def test_read_file(self):
        tn = tempfile.mktemp()
        tndir = os.path.dirname(tn)
        with open(tn, 'w') as f:
            f.write(TEST_CONFIG)

        d = configuration.read_configuration(tn)
        eq_(d['outfiles'],
            [os.path.normpath('/absolute/path1'),
             os.path.normpath(os.path.join(tndir, 'relative/path2'))])
        eq_(d['paths'],
            [os.path.normpath('/absolute/path3'),  # -- WINDOWS-REQUIRES: normpath
             os.path.normpath(os.path.join(tndir, 'relative/path4'))])
        eq_(d['format'], ['pretty', 'tag-counter'])
        eq_(d['tags'], ['@foo,~@bar', '@zap'])
        eq_(d['stdout_capture'], False)
        ok_('bogus' not in d)
        eq_(d['userdata'], [('foo', 'bar')])

    def test_userdata_is_appended(self):
        config = configuration.Configuration([
            "--define", "foo=foo_value",
            "--define=bar=bar_value",
        ])
        eq_("foo_value", config.userdata.foo)
        eq_("bar_value", config.userdata.bar)


class TestUserData(unittest.TestCase):
    def test_create_from_list_of_eq_separated_entries(self):
        userdata = configuration.UserData(["foo=bar=baz"])
        self.assertEqual("bar=baz", userdata.foo)

    def test_right_side_of_eq_separated_entry_may_be_empty(self):
        userdata = configuration.UserData(["foo", "bar="])
        self.assertEqual("", userdata.foo)
        self.assertEqual("", userdata.bar)

    def test_create_from_config_file_section_mixed_w_eq_separated_entries(self):
        userdata = configuration.UserData([
            ("foo", "foo_value"),
            "bar=bar_value",
        ])
        self.assertEqual("foo_value", userdata.foo)
        self.assertEqual("bar_value", userdata.bar)
