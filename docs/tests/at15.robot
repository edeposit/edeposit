*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  my-keywords.robot

Variables       variables.py
    
Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs
Library  OperatingSystem
    
*** Variables ***

*** Test Cases ***

UC15-01 Odevzdání dokumentu
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Odevzdání dokumentu
    Page Should Contain Element           css=input#form-widgets-isbn
    Page Should Contain Element           css=#form-buttons-odevzdat
    Input Text                            css=input#form-widgets-isbn      ${VALID_BUT_DUPLICIT_ISBN}
    Click Button                          Načíst záznam z Alephu
    Pause
    Add OriginalFile for ePublication
    Click Link                            css=#forms.buttons.save
    