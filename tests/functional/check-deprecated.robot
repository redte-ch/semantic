*** Settings ***
Documentation			Tests for the deprecation check.
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
	${result} =			Run PySemVer		--help	check-deprecated
	Wait For Process	pysemver
	Should Contain		${result.stdout}	Usage: pysemver check-deprecated [--options] …
	Should Contain		${result.stdout}	Check if there are features to deprecate.
	Should Contain		${result.stdout}	-i, --ignore
	Should Contain		${result.stdout}	Paths to ignore
	Should Contain		${result.stdout}	.editorconfig, .github
	Exit OK				${result.rc}
