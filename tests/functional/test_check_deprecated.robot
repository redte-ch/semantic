# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

*** Settings ***
Documentation			Tests for the deprecation check.
Library					Process
Suite Teardown			Terminate All Processes	kill=True

*** Keywords ***
Run Mantic
	[Arguments]			@{args}
	${result} =			Run Process
	...					poetry		run		mantic
	... 				@{args}
	...					alias=mantic
	...					env:COLUMNS=200
	...					stdout=.robot/stdout.txt
	[Return]			${result}

Exit OK
	[Arguments]								${exit_code}
	Should Be Equal As Integers				${exit_code}	0

*** Test Cases ***
Prints the help screen to the user.
	${result} =			Run Mantic		--help	check-deprecated
	Wait For Process	mantic
	Should Contain		${result.stdout}	Usage: mantic check-deprecated [--options] …
	Should Contain		${result.stdout}	Check if there are features to deprecate.
	Should Contain		${result.stdout}	-i, --ignore
	Should Contain		${result.stdout}	Paths to ignore
	Should Contain		${result.stdout}	.editorconfig, .github
	Exit OK				${result.rc}

Checks for required deprecations.
	${result} =			Run Mantic		check-deprecated
	Wait For Process	mantic
	Exit OK				${result.rc}
