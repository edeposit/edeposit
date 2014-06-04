*** Settings ***
Library    Selenium2Library    5    run_on_failure=Capture Page Screenshot
Library    Dialogs
Library    String
Library    amqp.RabbitMQ
Library    Collections

Test Setup      Open Browser      ${PLONE_URL}
Test Teardown   Run Keywords      Close Browser     Delete Test Queue
Variables       it_variables.py
Resource        my-keywords.robot
Resource        it-keywords.robot

*** Variables ***
${PLONE_URL}        http://edeposit-test.nkp.cz
    
*** Test Cases ***

UC02 Ohlášení ePublikace s anglickym ISBN a zobrazeni exception
    Declare Queue                    ${QUEUE_NAME}
    Declare Queue Binding            search    ${QUEUE_NAME}   *
    Registrace producenta
    Log in                           ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication    
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ENGLISH_ISBN}
    Fill inputs about Vydani
    Click Button                          form.buttons.save    
    Sleep     5s

    ${MSG}=                          Get Message From Queue          ${QUEUE_NAME}
    Log Dictionary                   ${MSG}   WARN
    ${MSG_BODY}=                     Get From Dictionary   ${MSG}   body
    ${MSG_HEADERS}=                  Get From Dictionary   ${MSG}   headers
    Dictionary Should Contain Item   ${MSG_BODY}   __nt_name   ISBNValidationResult
    Dictionary Should Contain Item   ${MSG_BODY}   is_valid    True

    ${MSG}=                          Get Message From Queue          ${QUEUE_NAME}
    Log Dictionary                   ${MSG}   WARN
    ${MSG_BODY}=                     Get From Dictionary   ${MSG}   body
    ${MSG_HEADERS}=                  Get From Dictionary   ${MSG}   headers
    Dictionary Should Contain Item   ${MSG_BODY}   __nt_name   CountResult
    Dictionary Should Contain Item   ${MSG_BODY}   num_of_records    0
    
    ${MSG}=                          Get Message From Queue          ${QUEUE_NAME}
    Log Dictionary                   ${MSG}   WARN
    ${MSG_BODY}=                     Get From Dictionary   ${MSG}   body
    ${MSG_HEADERS}=                  Get From Dictionary   ${MSG}   headers
    Dictionary Should Contain Item   ${MSG_HEADERS}   exception   Only czech ISBN is accepted!
    Dictionary Should Contain Item   ${MSG_HEADERS}   exception_type   <type 'exceptions.AssertionError'>
    Dictionary Should Contain Item   ${MSG_HEADERS}   exception_name   AssertionError
    Dictionary Should Contain Key    ${MSG_HEADERS}   UUID
    
    Zobrazit historii
    Sleep     1s
    Historie obsahuje zprávu         K akvizici
    Historie obsahuje zprávu         Poslal jsem jeden záznam k exportu do Alephu
    Historie obsahuje zprávu         Chyba ze služby Aleph
    Click Link                       Zobrazení
    Wait Until Page Contains         Export do Alephu



*** Keywords ***

Delete Test Queue
    Delete Queue     ${QUEUE_NAME}
        