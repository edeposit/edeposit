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

IT-Fix07 - Fix for UC01-07 Kontrola dostupnosti uzivatelskeho jmena pri jedne registraci
    Registrace producenta
    Click link        Registrovat
    Page Should Contain   		Registrace producenta
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator
    Click Button			Registrovat
    Pause
    Page should contain                 Prosím opravte vyznačené chyby.
    Page should contain                 Uživatelské jméno u správce producenta je již použito. Vyplňte jiné.
    Add one administrator
    Fill Unique UserName
    Click Button			Registrovat
    Wait Until Page Contains            Položka byla vytvořena
    
*** Keywords ***

