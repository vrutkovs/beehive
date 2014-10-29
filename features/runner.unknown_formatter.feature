Feature: When an unknown formatter is used


  Scenario: Unknown formatter is used
    When I run "beehive -f unknown1"
    Then it should fail with:
      """
      beehive: error: format=unknown1 is unknown
      """

  Scenario: Unknown formatter is used together with another formatter
    When I run "beehive -f plain -f unknown1"
    Then it should fail with:
      """
      beehive: error: format=unknown1 is unknown
      """

  Scenario: Two unknown formatters are used
    When I run "beehive -f plain -f unknown1 -f tags -f unknown2"
    Then it should fail with:
      """
      beehive: error: format=unknown1, unknown2 is unknown
      """
