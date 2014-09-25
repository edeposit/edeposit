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
#${PLONE_URL}        http://localhost:8080/edeposit
#${PLONE_URL}        http://edeposit-test.nkp.cz


*** Keywords ***


*** Test Cases ***

IT00 Instalace produktu
    # update security
    # rebuild catalog

IT02-01 Ohlášení se soubory
    Prepare AMQP Test Environment
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Ohlašovací lístek ISBN - ePublikace 
    Fill inputs about ePublication    
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ISBN}
    Click Button                          form.buttons.save    
    Page Should Contain                   Položka byla vytvořena
    Location Should Contain               lesni-skolky-ve-zline
    Page Should Contain                   Processing
    Sleep   1s
    Pause

IT02-02 Ohlášení se soubory s pridelenim ISBN
    Prepare AMQP Test Environment
    Open Browser with System User
    Reinstall E-Deposit modules  
    Switch Browser   1
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Ohlašovací lístek ISBN - ePublikace 
    Fill inputs about ePublication    
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication with ISBN generated
    Click Button                          form.buttons.save    
    Page Should Contain                   Položka byla vytvořena
    Location Should Contain               lesni-skolky-ve-zline
    Page Should Contain                   Processing
    Pause
    Wait Until Keyword Succeeds      10s  0.5s  ePublication contains Original File at state    isbngeneration
    Send email to ISBN Agency
    Switch Browser   1
    Pause
 
IT02-0a Ohlášení ePublikace - kontrola Aleph amqp sluzby
    Log    ${QUEUE_NAME}   WARN
    Declare Queue                    aleph  ${QUEUE_NAME}
    Declare Queue Binding            aleph  search    ${QUEUE_NAME}   *
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
    
IT02-03 Ohlášení ePublikace
    Registrace producenta
    Log in                           ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains Element      css=input[value="Ohlásit"]
    #Page Should Contain                   Pokud máte k dispozici originál ePublikace, nezapomeňte jej přiložit!
    #Page Should Contain                   Chcete odevzdat dokument k již ohlášené ePublikaci?
    Fill inputs about ePublication    
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ISBN}
    Fill inputs about Vydani
    Click Button                          form.buttons.save    
    Sleep     5s
    Zobrazit historii
    Pause
    Historie obsahuje zprávu         K akvizici
    Historie obsahuje zprávu         Poslal jsem jeden záznam k exportu do Alephu
    Historie obsahuje zprávu         Export jednoho záznamu do Alephu
    Historie obsahuje zprávu         Export jednoho záznamu do Alephu skončil s chybou
    Click Link                       Zobrazení
    Pause
    Wait Until Page Contains         Export do Alephu

IT02-04 Ohlášení ePublikace - Diazo Theme - kontrola online validace ISBN
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

IT02-05 Ohlášení ePublikace - Diazo Theme - odevzdání dokumentu k již ohlášené ePublikaci
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

IT02-06 Ohlášení ePublikace - Diazo Theme - odevzdání dokumentu s přidělením ISBN
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

IT02-07 Ohlášení ePublikace - Diazo Theme - odevzdání dokumentu s přidělením ISBN, zobrazeni chyby
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
