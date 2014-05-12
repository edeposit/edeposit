*** Settings ***
Library    Selenium2Library   5
Library    Dialogs
Library    String
Test Setup      Open Browser      ${PLONE_URL}
Test Teardown   Close Browser
Variables       variables.py
            
*** Variables ***
${PLONE_URL}        http://localhost:8080/Plone
${USER_PASSWORD}   fafs08ja
    
# ${TEST_SEED} ... nahodny string
    
*** Test Cases ***

# Registrace producenta - domovská stránka
#     Click link    Registrovat
#     Wait Until Page Contains   Registrace producenta
#     Page Should Contain    Producent    
#     Page Should Contain    Editoři producenta

# Registrace producenta - zobrazení chyb ve formuláři
#     Click link    Registrovat
#     Wait Until Page Contains   Registrace producenta
#     Click Button          Registrovat
#     Page Should Contain   Required input is missing.
#     Page Should Contain   Registrace producenta
#     Page Should Contain   Chyba
#     Page Should Contain   Prosím opravte vyznačené chyby.

Registrace producenta - registrace
    Click link    Registrovat
    Wait Until Page Contains   Registrace producenta
    Input Text                 css=#form-widgets-IBasic-title   Testovací producent ${TEST_SEED}
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-fullname    Testovaci uzivatel ${TEST_SEED}
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-email       stavel.jan@gmail.com
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-phone       733230772
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-username    test${TEST_SEED}
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-password    ${USER_PASSWORD}
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-password_ctl   ${USER_PASSWORD}
    Click Link                 Adresa
    Input Text                 css=#form-widgets-street    Pašovice 71
    Input Text                 css=#form-widgets-city      Prakšice
    Input Text                 css=#form-widgets-country   Česká republika
    Input Text                 css=#form-widgets-psc       73323072
    Click Button               Registrovat
    Pause

*** Keywords ***
