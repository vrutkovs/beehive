Feature: Basic directory layout (Variant 1B)

  As a story/test writer
  I want a simple, non-deep directory structure
  So that I can easily get an overview which stories/tests exist

  | BASIC DIRECTORY LAYOUT STRUCTURE:
  |     testing/features/
  |       +-- steps/*.py          # Step definitions or step-library imports.
  |       +-- *.feature           # Feature files.
  |       +-- environment.py      # OPTIONAL: environment setup/hooks.
  |
  | SEE ALSO:
  |   * http://pythonhosted.org/beehive/gherkin.html#layout-variations


    @setup
    Scenario: Setup directory structure
        Given a new working directory
        And a file named "testing/features/steps/steps.py" with:
            """
            from beehive import step

            @step('{word:w} step passes')
            def step_passes(context, word):
                pass

            @step('{word:w} step fails')
            def step_fails(context, word):
                assert False, "XFAIL-STEP"
            """
        And a file named "testing/features/alice.feature" with:
            """
            Feature: Alice
                Scenario: A1
                  Given a step passes
                  When another step passes
                  Then a step passes
            """
        And a file named "testing/features/bob.feature" with:
            """
            Feature: Bob
                Scenario: B1
                  When a step passes
                  Then another step passes
            """


    Scenario: Run beehive with testing directory
        When I run "beehive -f progress testing/"
        Then it should fail with:
            """
            ConfigError: No steps directory in "{__WORKDIR__}/testing"
            """

    Scenario: Run beehive with feature subdirectory
        When I run "beehive -f progress testing/features/"
        Then it should pass with:
            """
            2 features passed, 0 failed, 0 skipped
            2 scenarios passed, 0 failed, 0 skipped
            5 steps passed, 0 failed, 0 skipped, 0 undefined
            """

    Scenario: Run beehive with one feature file
        When I run "beehive -f progress testing/features/alice.feature"
        Then it should pass with:
            """
            1 feature passed, 0 failed, 0 skipped
            1 scenario passed, 0 failed, 0 skipped
            3 steps passed, 0 failed, 0 skipped, 0 undefined
            """


    Scenario: Run beehive with two feature files
        Given a file named "one.featureset" with:
            """
            testing/features/alice.feature
            testing/features/bob.feature
            """
        When I run "beehive -f progress @one.featureset"
        Then it should pass with:
            """
            2 features passed, 0 failed, 0 skipped
            2 scenarios passed, 0 failed, 0 skipped
            5 steps passed, 0 failed, 0 skipped, 0 undefined
            """
