*** Settings ***
Library             Process

*** Test Cases ***
Prints the home screen to the user.
  ${result} =       Run Process         poetry  run   pysemver  alias=proc  env:COLUMNS=200   stdout=.robot/stdout.txt
                    Wait For Process    proc
  Should Contain    ${result.stdout}    Usage: pysemver [--help] <command> …
  Should Contain    ${result.stdout}    check-deprecated
  Should Contain    ${result.stdout}    check-version
