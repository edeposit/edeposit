*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs

Variables  variables.py
Resource  my-keywords.robot
    
*** Variables ***
    
*** Keywords ***

*** Test Cases ***

Vytvoření akvizitora
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Overlay Button        Přidat nového uživatele
    Input Text       //input[@id='form.fullname']   Akvizitor
    Input Text       //input[@id='form.username']   ${AKVIZITOR_NAME}
    Input Text       //input[@id='form.email']      test@nkp.cz
    Input Text       //input[@id='form.password']   ${AKVIZITOR_PASSWORD}
    Input Text       //input[@id='form.password_ctl']   ${AKVIZITOR_PASSWORD}
    Select Checkbox  //input[@id='form.groups.1']
    Click Button     Registrovat
    Wait Until Page Contains    Přehled uživatelů
    User Should Exist       ${AKVIZITOR_NAME}
    User Can Log In         ${AKVIZITOR_NAME}    ${AKVIZITOR_PASSWORD}

Vytvoření RIV posuzovatele
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Overlay Button        Přidat nového uživatele
    Input Text       //input[@id='form.fullname']   RIV
    Input Text       //input[@id='form.username']   ${RIV_NAME}
    Input Text       //input[@id='form.email']      test@nkp.cz
    Input Text       //input[@id='form.password']   ${RIV_PASSWORD}
    Input Text       //input[@id='form.password_ctl']   ${RIV_PASSWORD}
    Select Checkbox  //input[@id='form.groups.8']
    Click Button     Registrovat
    Wait Until Page Contains    Přehled uživatelů
    User Should Exist       ${RIV_NAME}
    User Can Log In         ${RIV_NAME}    ${RIV_PASSWORD}

# Stránka pro RIV posuzovatele
#     Vytvoření RIV posuzovatele
#     Log In           riv  afado3
#     Page Should Contain    Přehledová stránka uživatele Jan Stavel
#     Pause
    
# Přehledová stránka posuzovatele od RIVu
#     Go to user page
#     Page Should Contain Link    ePublikace k posouzení RIVem
#     Pause

