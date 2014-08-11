*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs

Resource    my-keywords.robot
Variables   variables.py
        
*** Variables ***
    
*** Keywords ***

*** Test Cases ***

AT04-00 Příprava katalogizace
    Registrace producenta
    Log in                              ${USER_NAME}   ${USER_PASSWORD}
    Add more ePublications
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications
    Check two ePublications
    Click Button                        Přiřadit pracovníka
    Page Should Contain list of two ePublications
    Page Should Contain list of persons
    Select one person
    Click Button                        Potvrdit
