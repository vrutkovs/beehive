# -*- coding: utf-8 -*-
"""Step implementations for tutorial example."""

from beehive import given, when, then


@given('we have beehive installed')
def we_have_beehive_installed(context):
    pass


@when('we implement a test')
def we_implement_a_test(context):
    assert True is not False


@then('beehive will test it for us!')
def beehive_will_test_it_for_us(context):
    assert context.failed is False
