# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

*** Settings ***
Documentation			Tests for the semantic version check.
Library					Process
Suite Teardown			Terminate All Processes	kill=True

*** Keywords ***
Run PySemVer
	[Arguments]			@{args}
	${result} =			Run Process
	...					poetry		run		pysemver
	... 				@{args}
	...					alias=pysemver
	...					env:COLUMNS=200
	...					stdout=.robot/stdout.txt
	[Return]			${result}

Exit OK
	[Arguments]								${exit_code}
	Should Be Equal As Integers				${exit_code}	0

*** Test Cases ***
Prints the help screen to the user.
	${result} =			Run PySemVer		--help  check-version
	Wait For Process	pysemver
	Should Contain		${result.stdout}	Usage: pysemver check-version [--options] …
	Should Contain		${result.stdout}	Check if the actual version is valid.
	Should Contain		${result.stdout}	-i, --ignore
	Should Contain		${result.stdout}	Paths to ignore
	Should Contain		${result.stdout}	.editorconfig, .github
	Exit OK				${result.rc}

Checks for required version bump.
	${result} =			Run PySemVer		check-version
	Wait For Process	pysemver
	Exit OK				${result.rc}
