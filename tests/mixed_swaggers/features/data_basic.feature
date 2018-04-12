Feature: Basic operations on data in Oneprovider mixed tests scenarios

  Examples:
  | client1 | client2 	|
  | REST    | web GUI 	|
  | web GUI	| REST		|

  Background:
    Given initial users configuration in "z1" Onezone service:
            - user1
    And initial spaces configuration in "z1" Onezone service:
        space1:
            owner: user1
            providers:
                - p1:
                    storage: NFS
                    size: 1000000
                
    And opened browser with user1 logged to "z1 onezone" service
    And opened p1 Oneprovider view in web GUI by user1


  Scenario Outline: Create directory
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in p1 Oneprovider
    Then using <client2>, user1 succeeds to see item named "dir1" in "space1" in p1 Oneprovider


  Scenario Outline: Remove directory
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in p1 Oneprovider
    And using <client2>, user1 succeeds to see item named "dir1" in "space1" in p1 Oneprovider
	And using <client2>, user1 removes directory named "dir1" in "space1" in p1 Oneprovider
	Then using <client1>, user1 fails to see item named "dir1" in "space1" in p1 Oneprovider
	
  
Scenario Outline: Create file
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in p1 Oneprovider
    Then using <client2>, user1 succeeds to see item named "file1" in "space1" in p1 Oneprovider


  Scenario Outline: Remove file
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in p1 Oneprovider
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in p1 Oneprovider
	And using <client2>, user1 removes file named "file1" in "space1" in p1 Oneprovider
	Then using <client1>, user1 fails to see item named "file1" in "space1" in p1 Oneprovider


  Scenario Outline: Create directory structure
    When using <client1>, user1 creates directory structure in "space1" space on p1 Oneprovider as follow:
            - file1
            - dir1:
                - dir2:
                    - dir3
                    - dir4:
                        - file2
                        - file3
                        - dir5:
                            - dir6:
                                - dir7
                - dir8
                - file4
                - file5
                - dir9:
                    - file6
            - dir0 
    
    Then using <client2>, user1 sees that directory structure in "space1" space is as previously created
