*** Settings ***
Library             Process

*** Test Cases ***
Prints the help screen to the user.
  ${result} =       Run Process         poetry  run   pysemver  --help  check-version  alias=proc  env:COLUMNS=200   stdout=.robot/stdout.txt
                    Wait For Process    proc
  Should Contain    ${result.stdout}    Usage: pysemver check-version [--options] …
  Should Contain    ${result.stdout}    Check if the actual version is valid.
  Should Contain    ${result.stdout}    -i, --ignore
  Should Contain    ${result.stdout}    Paths to ignore
  Should Contain    ${result.stdout}    .editorconfig, .github
