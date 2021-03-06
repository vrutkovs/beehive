#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provide a beehive shell to simplify creation of feature files
and running features, etc.

    context.command_result = beehive_shell.beehive(cmdline, cwd=context.workdir)
    beehive_shell.create_scenario(scenario_text, cwd=context.workdir)
    beehive_shell.create_step_definition(context.text, cwd=context.workdir)
    context.command_result = beehive_shell.run_feature_with_formatter(
            context.features[0], formatter=formatter, cwd=context.workdir)

"""

from __future__ import print_function, with_statement
from beehive.compat import unicode, basestring
from beehive4cmd0.__setup import TOP
import os.path
import subprocess
import sys
import shlex
import codecs

# HERE = os.path.dirname(__file__)
# TOP  = os.path.join(HERE, "..")

# -----------------------------------------------------------------------------
# CLASSES:
# -----------------------------------------------------------------------------


class CommandResult(object):
    """
    ValueObject to store the results of a subprocess command call.
    """
    def __init__(self, **kwargs):
        self.command = kwargs.pop("command", None)
        self.returncode = kwargs.pop("returncode", 0)
        self.stdout = kwargs.pop("stdout", "")
        self.stderr = kwargs.pop("stderr", "")
        self._output = None
        if kwargs:
            names = ", ".join(kwargs.keys())
            raise ValueError("Unexpected: %s" % names)

    @property
    def output(self):
        if self._output is None:
            output = self.stdout
            if self.stderr:
                output += "\n"
                output += self.stderr
            self._output = output
        return self._output

    @property
    def failed(self):
        return not self.returncode

    def clear(self):
        self.command = None
        self.returncode = 0
        self.stdout = ""
        self.stderr = ""
        self._output = None


class Command(object):
    """
    Helper class to run commands as subprocess,
    collect their output and subprocess returncode.
    """
    DEBUG = False
    COMMAND_MAP = {
        "beehive": os.path.normpath("{0}/bin/beehive".format(TOP))
    }

    @classmethod
    def run(cls, command, cwd=".", **kwargs):
        """
        Make a subprocess call, collect its output and returncode.
        Returns CommandResult instance as ValueObject.
        """
        assert isinstance(command, basestring)
        command_result = CommandResult()
        command_result.command = command

        # -- BUILD COMMAND ARGS:
        if isinstance(command, unicode) and sys.version_info[0] == 2:
            command = codecs.encode(command)
        cmdargs = shlex.split(command)

        # -- TRANSFORM COMMAND (optional)
        real_command = cls.COMMAND_MAP.get(cmdargs[0], None)
        if real_command:
            cmdargs[0] = real_command

        if cmdargs[0].split('/')[-1] == 'beehive' and 'COVERAGE_FILE' in os.environ.keys():
            # Skip pypy - it takes ages on Travis to complete and generally useless
            if 'TRAVIS_PYTHON_VERSION' in os.environ.keys() and os.environ['TRAVIS_PYTHON_VERSION'] == 'pypy':
                pass
            else:
                import time
                os.environ['COVERAGE_FILE'] = '../.coverage.%d' % int(round(time.time() * 1000))
                cmdargs = ['coverage', 'run', '--branch'] + cmdargs

        # -- RUN COMMAND:
        try:
            process = subprocess.Popen(cmdargs,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True,
                                       cwd=cwd, **kwargs)
            out, err = process.communicate()
            if sys.version_info[0] < 3:  # py3: we get unicode strings, py2 not
                # XXX-DISABLED:
                # try:
                #    # jython may not have it
                #     default_encoding = sys.getdefaultencoding()
                # except AttributeError:
                #     default_encoding = sys.stdout.encoding or 'UTF-8'
                default_encoding = 'UTF-8'
                out = unicode(out, process.stdout.encoding or default_encoding)
                err = unicode(err, process.stderr.encoding or default_encoding)
            process.poll()
            assert process.returncode is not None
            command_result.stdout = out
            command_result.stderr = err
            command_result.returncode = process.returncode
            if cls.DEBUG:
                print("shell.cwd={0}".format(kwargs.get("cwd", None)))
                print("shell.command: {0}".format(" ".join(cmdargs)))
                print("shell.command.output:\n{0};".format(command_result.output))
        except OSError as e:
            command_result.stderr = u"OSError: %s" % e
            command_result.returncode = e.errno
            assert e.errno != 0
        return command_result


# -----------------------------------------------------------------------------
# FUNCTIONS:
# -----------------------------------------------------------------------------
def run(command, cwd=".", **kwargs):
    return Command.run(command, cwd=cwd, **kwargs)


def beehive(cmdline, cwd=".", **kwargs):
    """
    Run beehive as subprocess command and return process/shell instance
    with results (collected output, returncode).
    """
    assert isinstance(cmdline, basestring)
    return run("beehive " + cmdline, cwd=cwd, **kwargs)

# -----------------------------------------------------------------------------
# TEST MAIN:
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    command = " ".join(sys.argv[1:])
    output = Command.run(sys.argv[1:])
    print("command: {0}\n{1}\n".format(command, output))
