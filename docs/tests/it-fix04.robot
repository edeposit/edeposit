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

UC02 Ohlášení ePublikace - chybne zadana cena
    Registrace producenta
    Log in                           ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication    
    Input Text				css=#form-widgets-IBasic-title     Lesní školky ve Zlíně
    Input Text				css=#form-widgets-podnazev  Alternativní vzdělávání
    Fill cena        abca
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ISBN}
    Fill inputs about Vydani
    Click Button                          form.buttons.save    
    Element Text should be              css=.nazev > td:nth-child(3) > div:nth-child(1) > div:nth-child(1)     Zadaná hodnota není platné desetinné čislo.
    Fill cena        10
    Click Button                          form.buttons.save    
    Wait Until Page Contains              Položka byla vytvořena
    
*** Keywords ***

