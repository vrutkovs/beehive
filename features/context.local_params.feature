Feature: Local Context Parameters defined in Scenarios (Steps)

    | Specification:
    |   * When a step adds/modifies an attribute in the Context object,
    |     then its value is only available to other steps in this scenario.
    |   * After a scenario is executed all Context object changes are undone.

    Scenario: Add Local Context parameter in Scenario/Step
      Given the beehive context does not have a parameter "local_name"
      When I set the context parameter "local_name" to "Alice"
      Then the beehive context should have a parameter "local_name"
      And  the beehive context should contain:
        | Parameter  | Value   |
        | local_name | "Alice" |

    Scenario: Ensure that Local Context parameter is not available to next Scenario
      Then the beehive context should not have a parameter "local_name"
