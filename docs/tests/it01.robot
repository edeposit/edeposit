*** Settings ***
Library    Selenium2Library    5    run_on_failure=Capture Page Screenshot
Library    Dialogs
Library    String
Test Setup      Open Browser      ${PLONE_URL}
Test Teardown   Close Browser
Variables       it_variables.py
Resource        my-keywords.robot
Resource        it-keywords.robot

*** Variables ***
${PLONE_URL}        http://localhost:8080/Plone
${USER_PASSWORD}   fafs08ja
    
# ${TEST_SEED} ... nahodny string
    
*** Test Cases ***

Registrace producenta - domovská stránka
    Click link    Registrovat
    Wait Until Page Contains   Registrace producenta
    Page Should Contain    Producent    
    Page Should Contain    Editor producenta

Registrace producenta - zobrazení chyb ve formuláři
    Click link    Registrovat
    Wait Until Page Contains   Registrace producenta
    Click Button          Registrovat
    Page Should Contain   Required input is missing.
    Page Should Contain   Registrace producenta
    Page Should Contain   Chyba
    Page Should Contain   Prosím opravte vyznačené chyby.

Registrace producenta - registrace
    ${USER_NAME}=                    Catenate     SEPARATOR=-  test-user   ${TEST_SEED}  00
    Click link    Registrovat
    Wait Until Page Contains   Registrace producenta
    Input Text                 css=#form-widgets-IBasic-title   Testovací producent ${TEST_SEED}
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-fullname    Testovaci uzivatel ${TEST_SEED}
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-email       stavel.jan@gmail.com
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-phone       733230772
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-username    ${USER_NAME}
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-password    ${USER_PASSWORD}
    Input Text                 css=#form-widgets-IAdministrator-administrator-widgets-password_ctl   ${USER_PASSWORD}
    Click Link                 Adresa
    Input Text                 css=#form-widgets-street    Pašovice 71
    Input Text                 css=#form-widgets-city      Prakšice
    Input Text                 css=#form-widgets-country   Česká republika
    Input Text                 css=#form-widgets-psc       73323072
    Click Button               Registrovat
    Page Should Contain                 Vítejte!
    Page Should Contain                 Vaše uživatelská registrace proběhla.
    Log In                     ${USER_NAME}      ${USER_PASSWORD}
    Page Should Contain        Přehledová stránka uživatele
    Click Link                 Ohlášení ePublikací
    Page Should Contain        Ohlašovací lístek ISBN - ePublikace 

Registrace producenta - registrace s editorem
    ${USER_NAME}=                    Catenate     SEPARATOR=-  test-user        ${TEST_SEED}   01
    ${EDITOR1_NAME}=                 Catenate     SEPARATOR=-  test-editor1     ${TEST_SEED}   01
    Click link    Registrovat
    Wait Until Page Contains   Registrace producenta
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator
    Click Link                          Editor producenta
    Add one editor
    Click Button               Registrovat
    Page Should Contain                 Vítejte!
    Page Should Contain                 Vaše uživatelská registrace proběhla.
    Log In                     ${USER_NAME}      ${USER_PASSWORD}
    Page Should Contain        Přehledová stránka uživatele
    Click Link                 Ohlášení ePublikací
    Page Should Contain        Ohlašovací lístek ISBN - ePublikace
    Log out
    Log In                     ${EDITOR1_NAME}   ${EDITOR1_PASSWORD}
    Page Should Contain        Přehledová stránka uživatele
    Click Link                 Ohlášení ePublikací
    Page Should Contain        Ohlašovací lístek ISBN - ePublikace 
    
*** Keywords ***
