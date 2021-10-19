# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

*** Settings ***
Documentation 			Home screen tests.
Library					Process
Suite Teardown			Terminate All Processes	kill=True

*** Keywords ***
Run Mantic
	${result} =			Run Process
	...					poetry		run		mantic
	...					alias=mantic
	...					env:COLUMNS=200
	...					stdout=.robot/stdout.txt
	[Return]			${result}

Exit OK
	[Arguments]								${exit_code}
	Should Be Equal As Integers				${exit_code}	0

*** Test Cases ***
Prints the home screen to the user.
	${result} =			Run Mantic
	Wait For Process	mantic
	Should Contain		${result.stdout}	Usage: mantic [--help] <command> …
	Should Contain		${result.stdout}	check-deprecated
    Should Contain		${result.stdout}	check-version
    Exit OK				${result.rc}
