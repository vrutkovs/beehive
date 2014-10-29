@slow
Feature: Validate JSON Formatter Output

  As a tester
  I want that the JSON output is validated against its JSON schema
  So that the JSON formatter generates valid JSON output.

  | NOTES:
  |   Some have the beehive testruns may contain failures (@xfail).
  |   This should lead to more realistic JSON output, too.

  Scenario: Validate JSON output from features/ test run
    Given I use the current directory as working directory
    When I run "beehive -f json -o testrun1.json features/"
    When I run "bin/jsonschema_validate.py testrun1.json"
    Then it should pass with:
        """
        validate: testrun1.json ... OK
        """

  Scenario: Validate JSON output from issue.features/ test run
    Given I use the current directory as working directory
    When I run "beehive -f json -o testrun2.json issue.features/"
    When  I run "bin/jsonschema_validate.py testrun2.json"
    Then it should pass with:
        """
        validate: testrun2.json ... OK
        """

  Scenario: Validate JSON output from tools/test-features/ test run
    Given I use the current directory as working directory
    When I run "beehive -f json -o testrun3.json tools/test-features/"
    When I run "bin/jsonschema_validate.py testrun3.json"
    Then it should pass with:
        """
        validate: testrun3.json ... OK
        """