# -*- coding: utf-8 -*-
"""
Step definition for Context object tests.

EXAMPLE
    Scenario: Show that Context parameter
      Given I set the parameter "person" to "Alice" in the beehive context
      Then the beehive context should have a parameter named "person"
      And  the beehive context object should contain:
        | Parameter | Value   |
        | person    | "Alice" |

    Scenario: Show that Context parameter are not present in next scenario
      Then the beehive context should not have a parameter named "person"
"""

from beehive import given, when, then, step
from hamcrest import assert_that, equal_to

# -----------------------------------------------------------------------------
# STEPS:
# -----------------------------------------------------------------------------
@step(u'I set the context parameter "{param_name}" to "{value}"')
def step_set_beehive_context_parameter_to(context, param_name, value):
    setattr(context, param_name, value)

@step(u'the parameter "{param_name}" exists in the beehive context')
def step_beehive_context_parameter_exists(context, param_name):
    assert hasattr(context, param_name)

@step(u'the parameter "{param_name}" does not exist in the beehive context')
def step_beehive_context_parameter_not_exists(context, param_name):
    assert not hasattr(context, param_name)

@given(u'the beehive context has a parameter "{param_name}"')
def given_beehive_context_has_parameter_named(context, param_name):
    step_beehive_context_parameter_exists(context, param_name)

@given(u'the beehive context does not have a parameter "{param_name}"')
def given_beehive_context_does_not_have_parameter_named(context, param_name):
    step_beehive_context_parameter_not_exists(context, param_name)

@step(u'the beehive context should have a parameter "{param_name}"')
def step_beehive_context_should_have_parameter_named(context, param_name):
    step_beehive_context_parameter_exists(context, param_name)

@step(u'the beehive context should not have a parameter "{param_name}"')
def step_beehive_context_should_not_have_parameter_named(context, param_name):
    step_beehive_context_parameter_not_exists(context, param_name)

@then(u'the beehive context should contain')
def then_beehive_context_should_contain_with_table(context):
    assert context.table, "ENSURE: table is provided."
    for row in context.table.rows:
        param_name  = row["Parameter"]
        param_value = row["Value"]
        if param_value.startswith('"') and param_value.endswith('"'):
            param_value = param_value[1:-1]
        actual = str(getattr(context, param_name, None))
        assert hasattr(context, param_name)
        assert_that(actual, equal_to(param_value))

@given(u'the beehive context contains')
def given_beehive_context_contains_with_table(context):
    then_beehive_context_should_contain_with_table(context)