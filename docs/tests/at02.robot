*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  my-keywords.robot
Variables        variables.py
Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs
Library  OperatingSystem
Library  String
Library  amqp.RabbitMQ
Library  Collections
                
*** Variables ***

*** Test Cases ***

UC02-01 Domovská stránka uživatele
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Page Should Contain                   Přehledová stránka uživatele
    Page Should Contain                   Ohlášení ePublikace, ePeriodika, knihy
    Page Should Contain                   Vyhledat
    Page Should Contain                   Zlínsky vydavatel    

UC02-01 Ohlášení bez autoru
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Page Should Not Contain               Obsah
    Page Should Contain                   ePublikace
    Page Should Contain                   Název ePublikace
    Page Should Contain                   RIV
    Fill inputs about ePublication    
    Fill inputs about Vydani
    Add Original Files for ePublication   ${VALID_ISBN}
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena

UC02-01 Ohlášení se soubory
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Fill inputs about ePublication    
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ISBN}
    Click Button                          form.buttons.save    
    Page Should Contain                   Položka byla vytvořena
    Location Should Contain               lesni-skolky-ve-zline
    Page Should Contain                   Kontrola ISBN

UC02-01 Ohlášení s RIV kategorií
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Page Should Contain                   Ohlášení ePublikací
    Page Should Contain                   Ohlášování ePeriodik
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Fill inputs about ePublication    
    Fill inputs about ePublication    
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ISBN}
    Fill inputs about RIV    
    Click Button                          form.buttons.save    
    Page Should Contain                   Položka byla vytvořena
    RIV category should be selected

UC02-01 Nastavení kategorií pro RIV
    Log in as site owner
    Click Link                   admin
    Click Link                   Nastavení portálu
    Click Link                   css=a[href='${PLONE_URL}/portal_registry']
    Input Text                   name=q    RIV
    Click Element                css=input[value="Filter"]
    Click Link                   edeposit content categoriesForRIV
    Page Should Contain          Upravit záznam    

UC02-01 Existuje uživatel pro systémové akce
    Log in                             system    shoj98Phai9
    Page Should Contain                Přehledová stránka uživatele system

UC02-01 Ohlášení a odeslání k akvizici - stav Kontrola ISBN
    Stop Aleph daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Page Should Contain               Kontrola ISBN
    Page Should Not Contain           Přidat novou položku
    Page Should Not Contain           Úpravy
    
UC02-01 Historie akcí s ePublikací
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Click Link                        Historie
    Log                               Otevře se okno s historií akcí
    
UC02-01 Systémové zprávy ePublikace
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Page Should Contain                   Systémové zprávy
    Click Link                            Systémové zprávy
    Page Should Contain                   Systémové zprávy

UC02-01 Ohlášení a odeslání k akvizici - systemový uživatel může informovat o probíhajících akcích
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                        ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                         ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Page Should Contain               Lesní školky ve Zlíně
    Open Workflow Menu
    Click Element                     link=Oznámit systémovou akci

UC02-01 Start Aleph Daemon test
    Stop Aleph Daemon
    Sleep   1s
    ${output}=     Run    ps ax | grep alephdaemon
    Log        ${output}   WARN
    Should Not Contain    ${output}   edeposit_amqp_alephdaemon.py
    Start Aleph Daemon
    Sleep   1s
    ${output}=     Run    ps ax | grep alephdaemon
    Log        ${output}   WARN
    Should Contain        ${output}   edeposit_amqp_alephdaemon.py
    Stop Aleph Daemon
    Sleep   1s
    ${output}=     Run    ps ax | grep alephdaemon
    Log        ${output}   WARN
    Should Not Contain    ${output}   edeposit_amqp_alephdaemon.py

    
UC02-01 Jaké typy systémových zpráv systém generuje ve stavu Kontrola ISBN
    Start Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Click Link                            Systémové zprávy
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline/system-messages
    Open add new menu    
    Click Element                         link=ISBN Count Request
    Input Text                            css=#form-widgets-IBasic-title   Kontrola ISBN
    Input Text                            css=#form-widgets-isbn    fasdfasdfas
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena
    Click Link                            Systémové zprávy
    Open add new menu    
    Click Element                         link=ISBN Validation Request
    Input Text                            css=#form-widgets-IBasic-title   Kontrola duplicity ISBN
    Input Text                            css=#form-widgets-isbn    fasdfasdfas
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena
    Click Link                            Systémové zprávy
    Open add new menu    
    Click Element                         link=ISBN Count Result
    Input Text                            css=#form-widgets-IBasic-title   Kontrola duplicity ISBN
    Input Text                            css=#form-widgets-isbn    fasdfasdfas
    Input Text                            css=#form-widgets-num_of_records    10
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena
    Click Link                            Systémové zprávy
    Open add new menu
    Click Element                         link=ISBN Validation Result
    Input Text                            css=#form-widgets-IBasic-title   Kontrola duplicity ISBN
    Input Text                            css=#form-widgets-isbn    fasdfasdfas
    Select Checkbox                       css=#form-widgets-is_valid-0
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena
    Click Link                            Systémové zprávy
    Page Should Contain                   Kontrola ISBN
    Page Should Contain                   Výsledky dotazu na duplicitu ISBN
    Page Should Contain                   Kontrola duplicity ISBN
    Page Should Contain                   Výsledky kontroly ISBN

UC02-01 Po odeslání ePublikace k akvizici se objeví systémové zprávy
    Stop Aleph Daemon
    Start Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Sleep                                 5s
    Click Link                            Systémové zprávy
    Page Should Contain                   Kontrola ISBN:
    Page Should Contain                   Zjištění duplicity ISBN:
    Page Should Contain                   Výsledky kontroly ISBN
    Page Should Contain                   Výsledky dotazu na duplicitu ISBN
    Stop Aleph Daemon

UC02-01 Ohlaseni ePublikace - stav Antivirus
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=Všechna ISBN jsou v pořádku
    Page Should Contain                   Antivirová kontrola
    Log out
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Page Should Contain                   Antivirová kontrola
    Page Should Not Contain               Přidat novou položku
    Page Should Not Contain               Úpravy


UC02-01 Ohlaseni ePublikace - stav Antivirus - worfklow akce pro system
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=Všechna ISBN jsou v pořádku
    Open Workflow Menu
    Page Should Contain                   Žádný soubor neobsahuje virus
    Page Should Contain                   Antivirová kontrola jednoho souboru prošla
    Page Should Contain                   Antivirová kontrola jednoho souboru neprošla
    Page Should Contain                   Některý soubor obsahuje virus

UC02-01 Ohlaseni ePublikace - stav Generovani nahledu
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=Všechna ISBN jsou v pořádku
    Open Workflow Menu
    Click Element                         link=Žádný soubor neobsahuje virus
    Log out
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Page Should Contain                   Generování náhledů
    Page Should Not Contain               Přidat novou položku
    Page Should Not Contain               Úpravy


UC02-01 Ohlaseni ePublikace - stav Generovani nahledu - workflow akce pro system
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=Všechna ISBN jsou v pořádku
    Open Workflow Menu
    Click Element                         link=Žádný soubor neobsahuje virus
    Open Workflow Menu
    Page Should Contain Element           link=Máme všechny náhledy vygenerovány
    Page Should Contain Element           link=Generování některých náhledů skončilo s chybou
    Page Should Contain Element           link=Generování jednoho náhledu skončilo s chybou
    Page Should Contain Element           link=Generování jednoho náhledu proběhlo úspěšně


UC02-01 Ohlaseni ePublikace - stav Export do Alephu
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=Všechna ISBN jsou v pořádku
    Open Workflow Menu
    Click Element                         link=Žádný soubor neobsahuje virus
    Open Workflow Menu
    Click Element                         link=Máme všechny náhledy vygenerovány
    Log out
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Page Should Contain                   Export do Alephu
    Page Should Not Contain               Přidat novou položku
    Page Should Not Contain               Úpravy

UC02-01 Ohlaseni ePublikace - stav Export do Alephu - systemove akce
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=Všechna ISBN jsou v pořádku
    Open Workflow Menu
    Click Element                         link=Žádný soubor neobsahuje virus
    Open Workflow Menu
    Click Element                         link=Máme všechny náhledy vygenerovány
    Page Should Contain                   Export do Alephu
    Open Workflow Menu
    Page Should Contain Element           link=Poslal jsem jeden záznam k exportu do Alephu
    Page Should Contain Element           link=Export jednoho záznamu do Alephu skončil s chybou
    Page Should Contain Element           link=Export jednoho záznamu do Alephu proběhl úspěšně
    Page Should Contain Element           link=Všechny exporty do Alephu proběhly úspěšně
    Page Should Contain Element           link=Některé exporty do Alephu skončily s chybou


UC02-01 Ohlaseni ePublikace - Export do Alephu - systemove zpravy
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=Všechna ISBN jsou v pořádku
    Open Workflow Menu
    Click Element                         link=Žádný soubor neobsahuje virus
    Open Workflow Menu
    Click Element                         link=Máme všechny náhledy vygenerovány
    Click Link                            Systémové zprávy
    Open add new menu    
    Click Element                         link=Aleph Export Request
    Input Text                            css=#form-widgets-IBasic-title     Zaznam k exportu do Alephu
    Input Text                            css=#form-widgets-originalFileID   inzlin-01-2013-s-nasi-tabinkou.pdf
    Input Text                            css=#form-widgets-isbn             isbn-fadsfaljfa
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena
    Click Link                            Systémové zprávy
    Open add new menu
    Click Element                         link=Aleph Export Result
    Input Text                            css=#form-widgets-IBasic-title   Vysledek exportu do Alephu
    Input Text                            css=#form-widgets-isbn           isbn-fadsfjasd
    Click Button                          form.buttons.save
    Page Should Contain                   Položka byla vytvořena

UC02-01 Ohlaseni ePublikace - stav Čekání na Aleph
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=Všechna ISBN jsou v pořádku
    Open Workflow Menu
    Click Element                         link=Žádný soubor neobsahuje virus
    Open Workflow Menu
    Click Element                         link=Máme všechny náhledy vygenerovány
    Open Workflow Menu
    Click Element                         link=Všechny exporty do Alephu proběhly úspěšně
    Log out
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Page Should Contain                   Čekání na Aleph
    Page Should Not Contain               Přidat novou položku
    Page Should Not Contain               Úpravy

UC02-01 Ohlaseni ePublikace - stav Příprava akvizice - systémové akce
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=Všechna ISBN jsou v pořádku
    Open Workflow Menu
    Click Element                         link=Žádný soubor neobsahuje virus
    Open Workflow Menu
    Click Element                         link=Máme všechny náhledy vygenerovány
    Open Workflow Menu
    Click Element                         link=Všechny exporty do Alephu proběhly úspěšně
    Click Link                            Systémové zprávy
    Open add new menu    
    Click Element                         link=Aleph Search SysNumber Request
    Input Text                            css=#form-widgets-IBasic-title     Zaznam k dohledání SysNumber v Alephu
    Input Text                            css=#form-widgets-isbn           isbn-fadsfjasd
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena

UC02-01 Ohlášení se soubory - s aktivnim pripojenim do Alephu
    Open Browser with RabbitMQ
    Switch Browser      1
    Start Aleph Daemon
    Declare Queue                    ${QUEUE_NAME}
    Declare Queue Binding            search    ${QUEUE_NAME}   *
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Sleep    5s
    ISBNValidationResult is at RabbitMQ Test Queue
    CountResult is at RabbitMQ Test Queue
    Zobrazit historii
    Historie obsahuje zprávu             Poslal jsem jeden záznam k exportu do Alephu
    Historie obsahuje zprávu             Export jednoho záznamu do Alephu
    Stop Aleph Daemon
    Delete Test Queue

UC02-01 Ohlášení se soubory - s aktivnim pripojenim do Alephu a zobrazenim chyby z Alephu
    Start Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory a anglickym ISBN
    Sleep    5s
    Zobrazit historii
    Historie obsahuje zprávu             Poslal jsem jeden záznam k exportu do Alephu
    Historie obsahuje zprávu             Export jednoho záznamu do Alephu skon?il s chybou
    Historie obsahuje zprávu             Chyba p?i volání služby Aleph
    Stop Aleph Daemon

UC02-01 Ohlášení se soubory - kontrola online isbn kontroly
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Fill inputs about ePublication        
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${WRONG_ISBN}
    Page Should Contain                   chyba v isbn
    Click Button                          form.buttons.cancel
    Page Should Contain                   Ohlášení bylo přerušeno.
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/add-at-once
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Fill inputs about ePublication        
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_BUT_DUPLICIT_ISBN}
    Page Should Contain                   isbn je už použito. Použijte jíné, nebo nahlašte opravu.

