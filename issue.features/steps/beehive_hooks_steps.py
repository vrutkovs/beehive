# -*- coding: utf-8 -*-
from beehive import then

@then('the beehive hook "{hook}" was called')
def step_beehive_hook_was_called(context, hook):
    substeps = u'Then the command output should contain "hooks.{0}: "'.format(hook)
    context.execute_steps(substeps)

