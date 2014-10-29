@issue
Feature: Issue #75: beehive @features_from_text_file does not work

   | Feature of Cucumber. Reading the source code, I see it partly implemented.
   |
   |   $ beehive @list_of_features.txt
   |   https://github.com/jeamland/beehive/blob/master/beehive/runner.py#L416:L430
   |
   | However it fails because:
   |  * it does not remove the @ from the path
   |  * it does not search the steps/ directory in the parents of the feature files themselves


  @reuse.colocated_test
  Scenario: Use feature listfile
    Given I use the current directory as working directory
    When I run "beehive -f plain features/runner.feature_listfile.feature"
    Then it should pass
