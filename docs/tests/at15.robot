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
    Page Should Contain                   css=input#isbn
    Page Should Contain                   css=#forms.button.submit
    Input Text                            css=input#isbn      ${VALID_BUT_DUPLICIT_ISBN}
    Click Button                          Načíst záznam z Alephu
    Wait Until Page Contain               Odevzdat
    Add OriginalFile for ePublication
    Click Link                            css=#forms.buttons.save
    