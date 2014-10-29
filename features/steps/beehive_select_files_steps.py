# -*- coding: utf-8 -*-
"""
Provides step definitions that test how the beehive runner selects feature files.

EXAMPLE:
    Given beehive has the following feature fileset:
      '''
      features/alice.feature
      features/bob.feature
      features/barbi.feature
      '''
    When beehive includes feature files with "features/a.*\.feature"
    And  beehive excludes feature files with "features/b.*\.feature"
    Then the following feature files are selected:
      '''
      features/alice.feature
      '''
"""

from beehive import given, when, then
from beehive.runner_util import FeatureListParser
from hamcrest import assert_that, equal_to
from copy import copy
import re

# -----------------------------------------------------------------------------
# STEP UTILS:
# -----------------------------------------------------------------------------
class BasicBehaveRunner(object):
    def __init__(self, config=None):
        self.config = config
        self.feature_files = []

    def select_files(self):
        """
        Emulate beehive runners file selection by using include/exclude patterns.
        :return: List of selected feature filenames.
        """
        selected = []
        for filename in self.feature_files:
            if not self.config.exclude(filename):
                selected.append(str(filename))
        return selected

# -----------------------------------------------------------------------------
# STEP DEFINITIONS:
# -----------------------------------------------------------------------------
@given('beehive has the following feature fileset')
def step_given_beehive_has_feature_fileset(context):
    assert context.text is not None, "REQUIRE: text"
    beehive_runner = BasicBehaveRunner(config=copy(context.config))
    beehive_runner.feature_files = FeatureListParser.parse(context.text)
    context.beehive_runner = beehive_runner

@when('beehive includes all feature files')
def step_when_beehive_includes_all_feature_files(context):
    assert context.beehive_runner, "REQUIRE: context.beehive_runner"
    context.beehive_runner.config.include_re = None

@when('beehive includes feature files with "{pattern}"')
def step_when_beehive_includes_feature_files_with_pattern(context, pattern):
    assert context.beehive_runner, "REQUIRE: context.beehive_runner"
    context.beehive_runner.config.include_re = re.compile(pattern)

@when('beehive excludes no feature files')
def step_when_beehive_excludes_no_feature_files(context):
    assert context.beehive_runner, "REQUIRE: context.beehive_runner"
    context.beehive_runner.config.exclude_re = None

@when('beehive excludes feature files with "{pattern}"')
def step_when_beehive_excludes_feature_files_with_pattern(context, pattern):
    assert context.beehive_runner, "REQUIRE: context.beehive_runner"
    context.beehive_runner.config.exclude_re = re.compile(pattern)

@then('the following feature files are selected')
def step_then_feature_files_are_selected_with_text(context):
    assert context.text is not None, "REQUIRE: text"
    assert context.beehive_runner, "REQUIRE: context.beehive_runner"
    selected_files = context.text.strip().splitlines()
    actual_files = context.beehive_runner.select_files()
    assert_that(actual_files, equal_to(selected_files))
