*** Settings ***
Library    Selenium2Library    5    run_on_failure=Capture Page Screenshot
Library    Dialogs
Library    String
Library    amqp.RabbitMQ
Library    Collections
    
Test Setup      Open Browser      ${PLONE_URL}
Test Teardown   Close Browser
Variables       it_variables.py
Resource        my-keywords.robot
Resource        it-keywords.robot

*** Variables ***
${PLONE_URL}    http://localhost:8080/Plone
    
*** Test Cases ***

IT-Fix07 - Fix for UC01-05 Registrace producenta s editorem - kontrola povinnych policek, shodnosti hesel
    Click link                          Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-fullname     Jan Stavěl
    Click Button			Registrovat
    Page Should Contain                 Prosím opravte vyznačené chyby.
    Page Should Contain                 Některé položky u editora nejsou vyplněny. Buď vyplňte editorovi všechny položky, nebo je všechny smažte.
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password      ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl    ${USER_PASSWORD}
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-email   stavel.jan@gmail.com
    Click Button			Registrovat
    Page Should Contain                 Prosím opravte vyznačené chyby.
    Page Should Contain                 Některé položky u editora nejsou vyplněny. Buď vyplňte editorovi všechny položky, nebo je všechny smažte.
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password      ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl    ${USER_PASSWORD}
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-phone   773230772
    Input Text                          css=#form-widgets-IEditor-username   ${EDITOR1_NAME}
    Input Text                          css=#form-widgets-IEditor-password   ${EDITOR1_PASSWORD}
    Click Button			Registrovat
    Page Should Contain                 Prosím opravte vyznačené chyby.
    Page Should Contain                 Některé položky u editora nejsou vyplněny. Buď vyplňte editorovi všechny položky, nebo je všechny smažte.
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password      ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl    ${USER_PASSWORD}
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-password   ${EDITOR1_PASSWORD}
    Input Text                          css=#form-widgets-IEditor-password_ctl   wrongpassword
    Click Button			Registrovat
    Page Should Contain                 Prosím opravte vyznačené chyby.
    Page Should Contain                 U editora se neshodují zadaná hesla. Vyplňte hesla znovu.
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password      ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl    ${USER_PASSWORD}
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-password       ${EDITOR1_PASSWORD}
    Input Text                          css=#form-widgets-IEditor-password_ctl   ${EDITOR1_PASSWORD}
    Click Button			Registrovat
    Page Should Contain                 Vítejte!
    Page Should Contain                 Vaše uživatelská registrace proběhla.
    
*** Keywords ***

