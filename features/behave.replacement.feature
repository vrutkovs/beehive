Feature: Behave replacement

  As a story/test writer
  I want to seamlessly replace behave
  So that I can easily use the same module name for beehive

    @setup
    Scenario: Setup directory structure
        Given a new working directory
        And a file named "features/steps/behave_steps.py" with:
            """
            from behave import step

            @step('a step passes')
            def step_passes(context):
                pass
            """
        And a file named "features/steps/beehive_steps.py" with:
            """
            from beehive import step

            @step('another step passes')
            def another_step_passes(context):
                pass
            """
        And a file named "features/alice.feature" with:
            """
            Feature: Alice
                Scenario: A1
                  Given a step passes
                  When another step passes
                  Then a step passes
            """
        And a file named "features/bob.feature" with:
            """
            Feature: Bob
                Scenario: B1
                  When a step passes
                  Then another step passes
            """

    Scenario: Run beehive with feature directory
        When I run "beehive -f progress features/"
        Then it should pass with:
            """
            2 features passed, 0 failed, 0 skipped
            2 scenarios passed, 0 failed, 0 skipped
            5 steps passed, 0 failed, 0 skipped, 0 undefined
            """

    Scenario: Run beehive with one feature file
        When I run "beehive -f progress features/alice.feature"
        Then it should pass with:
            """
            1 feature passed, 0 failed, 0 skipped
            1 scenario passed, 0 failed, 0 skipped
            3 steps passed, 0 failed, 0 skipped, 0 undefined
            """


    Scenario: Run beehive with two feature files
        When I run "beehive -f progress features/alice.feature features/bob.feature"
        Then it should pass with:
            """
            2 features passed, 0 failed, 0 skipped
            2 scenarios passed, 0 failed, 0 skipped
            5 steps passed, 0 failed, 0 skipped, 0 undefined
            """
