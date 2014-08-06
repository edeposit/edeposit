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

UC02 Ohlášení ePublikace - chybne zadany rok
    Registrace producenta
    Log in                           ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication    
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ISBN}
    Fill inputs about Vydani
    Input Text                            css=#form-widgets-rok_vydani                  wrong year
    Click Button                          form.buttons.save    
    Element Text should be                css=.rok-vydani > td:nth-child(1) > div.fieldErrorBox > div.error     Zadaná hodnota není platné celé čislo.
    Input Text                            css=#form-widgets-rok_vydani                  2014
    Click Button                          form.buttons.save    
    Wait Until Page Contains              Položka byla vytvořena
    
*** Keywords ***

