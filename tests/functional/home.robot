*** Settings ***
Library   Process

*** Test Cases ***
Prints the home screen to the user
  ${result} =   Run Process   poetry  run   pysemver
  Should Contain  ${result.stdout}  Usage: pysemver [--help] <command> …
  Should Contain  ${result.stdout}  check-deprecated
  Should Contain  ${result.stdout}  check-version
