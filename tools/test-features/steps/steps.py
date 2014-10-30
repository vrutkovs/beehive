import logging
from beehive import given, when, then

spam_log = logging.getLogger('spam')
ham_log = logging.getLogger('ham')


@given("I am testing stuff")
def step_I_am_testing_stuff(context):
    context.testing_stuff = True


@given("some stuff is set up")
def step_some_stuff_is_set_up(context):
    context.stuff_set_up = True


@given("stuff has been set up")
def step_stuff_has_been_set_up(context):
    assert context.testing_stuff is True
    assert context.stuff_set_up is True


@when("I exercise it work")
def step_I_exercise_it_work(context):
    spam_log.error('logging!')
    ham_log.error('logging!')


@then("it will work")
def step_it_will_work(context):
    pass


@given("some text {prefix}")
def step_some_text_prefix(context, prefix):
    context.prefix = prefix


@when('we add some text {suffix}')
def step_we_add_some_text(context, suffix):
    context.combination = context.prefix + suffix


@then('we should get the {combination}')
def step_we_should_get_combination(context, combination):
    assert context.combination == combination


@given('some body of text')
def step_some_body_of_text(context):
    assert context.text
    context.saved_text = context.text

TEXT = '''   Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed
do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat.'''


@then('the text is as expected')
def step_text_is_as_expected(context):
    assert context.saved_text, 'context.saved_text is %r!!' % (context.saved_text, )
    context.saved_text.assert_equals(TEXT)


@given('some initial data')
def step_some_initial_data(context):
    assert context.table
    context.saved_table = context.table

TABLE_DATA = [
    dict(name='Barry', department='Beer Cans'),
    dict(name='Pudey', department='Silly Walks'),
    dict(name='Two-Lumps', department='Silly Walks'),
]


@then('we will have the expected data')
def step_we_will_have_expected_data(context):
    assert context.saved_table, 'context.saved_table is %r!!' % (context.saved_table, )
    for expected, got in zip(TABLE_DATA, iter(context.saved_table)):
        assert expected['name'] == got['name']
        assert expected['department'] == got['department']


@then('the text is substituted as expected')
def step_text_is_substituted_as_expected(context):
    assert context.saved_text, 'context.saved_text is %r!!' % (context.saved_text, )
    expected = TEXT.replace('ipsum', context.active_outline['ipsum'])
    context.saved_text.assert_equals(expected)


TABLE_DATA = [
    dict(name='Barry', department='Beer Cans'),
    dict(name='Pudey', department='Silly Walks'),
    dict(name='Two-Lumps', department='Silly Walks'),
]


@then('we will have the substituted data')
def step_we_will_have_the_substituted_data(context):
    assert context.saved_table, 'context.saved_table is %r!!' % (context.saved_table, )
    value = context.active_outline['spam']
    expected = value + ' Cans'
    assert context.saved_table[0]['department'] == expected, '%r != %r' % (
        context.saved_table[0]['department'], expected)


@given('the tag "{tag}" is set')
def step_tag_is_set(context, tag):
    assert tag in context.tags, '%r NOT present in %r!' % (tag, context.tags)
    if tag == 'spam':
        assert context.is_spammy


@given('the tag "{tag}" is not set')
def step_tag_is_not_set(context, tag):
    assert tag not in context.tags, '%r IS present in %r!' % (tag, context.tags)


@given('a string {argument} an argument')
def step_a_string_an_argument(context, argument):
    context.argument = argument

from beehive.matchers import register_type
register_type(custom=lambda s: s.upper())


@given('a string {argument:custom} a custom type')
def step_string_a_custom_type(context, argument):
    context.argument = argument


@then('we get "{argument}" parsed')
def step_we_get_argument_parsed(context, argument):
    assert context.argument == argument
