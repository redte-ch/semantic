*** Settings ***
Library   Process

*** Test Cases ***
Prints the home screen to the user
  ${result} =   Run Process   poetry  run   pysemver
  Should Not Contain  ${result.stderr}  AttributeError
