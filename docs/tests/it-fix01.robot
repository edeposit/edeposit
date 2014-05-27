*** Settings ***
Library    Selenium2Library    5    run_on_failure=Capture Page Screenshot
Library    Dialogs
Library    String
Test Setup      Open Browser      ${PLONE_URL}
Test Teardown   Close Browser
Variables       it_variables.py
Resource       it-keywords.robot

*** Variables ***
${PLONE_URL}        http://edeposit-test.nkp.cz
    
*** Test Cases ***

Pridavani noveho uzivatele
    Log In as Admin
    Go to   ${PLONE_URL}/@@usergroup-userprefs
    Click Button    Přidat nového uživatele
    Sleep   1s    
    Page Should Not Contain   Omlouváme se, ale zřejmě došlo k chybě...
    Page Should Contain     Přidat uživatlele
