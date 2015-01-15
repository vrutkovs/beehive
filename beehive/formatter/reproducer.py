# -*- coding: utf-8 -*-

from beehive.formatter.base import Formatter
import inspect
import re


class ReproducerFormatter(Formatter):
    name = "reproducer"
    description = "Script creating formatter"

    def __init__(self, stream_opener, config, **kwargs):
        super(ReproducerFormatter, self).__init__(stream_opener, config)
        self.stream = self.open()
        self.steps = []

    def match(self, match):
        self.steps.append(match)

    def close(self):
        # Write a python encoding
        self.stream.write('# -*- coding: utf-8 -*-\n\n')

        # Make a fake context object
        self.stream.write('context = object()\n\n')

        # before_all
        for match in self.steps:
            self.write_code_for_function(match)

    def write_code_for_function(self, match):
        self.stream.write('\n')

        # Print func arguments first
        for arg in match.arguments:
            self.stream.write("%s='%s'\n" % (arg.name, arg.value))

        func_lines = inspect.getsourcelines(match.func)[0]
        # Detect identation
        ident_size = len(re.compile('([\t ]*)').match(func_lines[2]).group())
        for line in func_lines[2:]:
            self.stream.write(line[ident_size:])

        # Unset arguments
        for arg in match.arguments:
            self.stream.write("del %s" % arg.name)

        self.stream.write('\n')
