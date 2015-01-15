# -*- coding: utf-8 -*-

from beehive.formatter.base import Formatter
import inspect
import re
import importlib
import types
import os


class ReproducerFormatter(Formatter):
    name = "reproducer"
    description = "Script creating formatter"

    def __init__(self, stream_opener, config, **kwargs):
        super(ReproducerFormatter, self).__init__(stream_opener, config)
        self.stream = self.open()
        self.steps = []

        self.hooks = self._import_hooks(config.env_py)
        self.imports = self._get_step_imports(config.env_py, config.steps_dir)

    def match(self, match):
        self.steps.append(match)

    def close(self):
        # Write a python encoding
        self.stream.write('# -*- coding: utf-8 -*-\n\n')

        # Paste collected imports
        [self.stream.write(line) for line in self.imports]
        self.stream.write('\n\n')

        # Make a fake context object
        self.stream.write('context = object()\n\n')

        self.stream.write(self.hooks['before_all'])
        for match in self.steps:
            self.stream.write(self.hooks['before_step'])
            self._write_code_for_function(match)
            self.stream.write(self.hooks['after_step'])
        self.stream.write(self.hooks['after_all'])

    def _load_module(self, file_path):
        # Import and parse environment.py
        # This is EXTREMELY dangerous - and I'm ashamed of that
        path, _ = os.path.splitext(file_path)
        file_name = path.split('/')[-1]
        return importlib.import_module(file_name, path)

    def _get_step_imports(self, env_file_path, steps_dir_path):
        files = ['features/%s' % env_file_path]
        imports = []

        # Make a list of files with steps
        for dirpath, dirnames, filenames in os.walk('features/%s' % steps_dir_path):
            for filename in [f for f in filenames if f.endswith(".py")]:
                files.append(os.path.join(dirpath, filename))

        for step_file in files:
            # Load direct imports
            try:
                with open(step_file) as f:
                    content = f.readlines()
                    for line in content:
                        if line.startswith('from ') or line.startswith('import '):
                            imports.append(line)
            except IOError:
                pass
        return imports

    def _import_hooks(self, env_file_path):
        hooks = {}
        known_hooks = ['before_all', 'after_all', 'before_step', 'after_step']

        env_file = self._load_module(env_file_path)
        funcs = [x for x in dir(env_file) if isinstance(getattr(env_file, x), types.FunctionType)]
        for hook_name in known_hooks:
            func_code = ''
            if hook_name in funcs:
                func = getattr(env_file, 'before_all')
                func_code = inspect.getsourcelines(func)[0]
                # Skip function declaration and unindent
                func_code = ''.join(self._strip_ident(func_code[1:]))
            hooks[hook_name] = func_code
        return hooks

    def _strip_ident(self, lines):
        ident_size = len(re.compile('([\t ]*)').match(lines[0]).group())
        new_lines = []
        for line in lines:
            new_lines.append(line[ident_size:])
        return new_lines

    def _write_code_for_function(self, match):
        self.stream.write('\n')

        # Print func arguments first
        for arg in match.arguments:
            self.stream.write("%s = '%s'\n" % (arg.name, arg.value))

        func_lines = inspect.getsourcelines(match.func)[0]
        # Strip decorator, func declaration and detect identation
        func_lines = self._strip_ident(func_lines[2:])
        [self.stream.write(line) for line in func_lines]

        # Unset arguments
        for arg in match.arguments:
            self.stream.write("del %s" % arg.name)

        self.stream.write('\n')