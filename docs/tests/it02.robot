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
${PLONE_URL}        http://localhost:8080/Plone
#${PLONE_URL}        http://edeposit-test.nkp.cz
# ${TEST_SEED} ... nahodny string
    
*** Test Cases ***

UC00 Instalace produktu
    # update security
    # rebuild catalog

UC02 Ohlášení ePublikace - kontrola Aleph amqp sluzby
    Declare Queue                    ${QUEUE_NAME}
    Declare Queue Binding            search    ${QUEUE_NAME}   *
    Registrace producenta
    Log in                           ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication    
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ISBN}
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
    Delete Queue                     ${QUEUE_NAME}
    
UC02 Ohlášení ePublikace
    Registrace producenta
    Log in                           ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Page Should Contain                   Pokud máte k dispozici originál ePublikace, nezapomeňte jej přiložit!
    Page Should Contain                   Chcete odevzdat dokument k již ohlášené ePublikaci?
    Fill inputs about ePublication    
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ISBN}
    Fill inputs about Vydani
    Pause
    Click Button                          form.buttons.save    
    Sleep     5s
    Zobrazit historii
    Sleep     1s
    Historie obsahuje zprávu         K akvizici
    Historie obsahuje zprávu         Poslal jsem jeden záznam k exportu do Alephu
    Historie obsahuje zprávu         Export jednoho záznamu do Alephu
    Historie obsahuje zprávu         Export jednoho záznamu do Alephu skončil s chybou
    Click Link                       Zobrazení
    Wait Until Page Contains         Export do Alephu

UC02 Ohlášení ePublikace - Diazo Theme - kontrola online validace ISBN
    ${USER_NAME}=                    Catenate     SEPARATOR=-  test-user   ${TEST_SEED}  01
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication        
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${WRONG_ISBN}
    Wait Until Page Contains              chyba v isbn
    Click Button                          form.buttons.cancel
    Wait Until Page Contains              Ohlášení bylo přerušeno.
    Go to                                 ${PLONE_URL}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication        
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_BUT_DUPLICIT_ISBN}
    Wait Until Page Contains              isbn je už použito. Použijte jíné, nebo nahlašte opravu.

UC02 Ohlášení ePublikace - Diazo Theme - odevzdání dokumentu k již ohlášené ePublikaci
    ${USER_NAME}=                    Catenate     SEPARATOR=-  test-user   ${TEST_SEED}  01
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication        
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_BUT_DUPLICIT_ISBN}
    Wait Until Page Contains              isbn je už použito. Použijte jíné, nebo nahlašte opravu.
    Pause

UC02 Ohlášení ePublikace - Diazo Theme - odevzdání dokumentu s přidělením ISBN
    ${USER_NAME}=                    Catenate     SEPARATOR=-  test-user   ${TEST_SEED}  01
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication        
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication with ISBN generated
    Click Button                          form.buttons.save    
    Wait Until Page Contains              Položka byla vytvořena
    Page Should Contain                   Přidělení ISBN

UC02 Ohlášení ePublikace - Diazo Theme - odevzdání dokumentu s přidělením ISBN, zobrazeni chyby
    ${USER_NAME}=                    Catenate     SEPARATOR=-  test-user   ${TEST_SEED}  01
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    Fill inputs about ePublication        
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Input Text                          css=#form-widgets-IOriginalFile-url  http://www.grada.cz/book/1000
    Choose File                         css=#form-widgets-IOriginalFile-file-input  /opt/edeposit/docs/tests/resources/inzlin-01-2013-s-nasi-Tabinkou.pdf
    UnSelect Checkbox                     css=#form-widgets-IOriginalFile-generated_isbn-0
    Click Button                          form.buttons.save    
    Wait Until Page Contains              Prosím opravte vyznačené chyby.
    Page Should Contain                   Buď zadejte ISBN, nebo vyberte - Přiřadit ISBN. V tom případě Vám ISBN přiřadí agentura
    Input Text                            css=input[id="form-widgets-IBasic-title"]   ${empty}
    Click Button                          form.buttons.save    
    Wait Until Page Contains              Prosím opravte vyznačené chyby.
    Page Should Contain                   Položka je povinná, zadejte hodnotu.

*** Keywords ***
