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

# AT02-01 Domovská stránka uživatele
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Page Should Contain                   Přehledová stránka uživatele
#     Page Should Contain                   Ohlášení ePublikace, ePeriodika, knihy
#     Page Should Contain                   Vyhledat
#     Page Should Contain                   Zlínsky vydavatel    

# AT02-02 Ohlášení bez autoru
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Page Should Not Contain               Obsah
#     Page Should Contain                   ePublikace
#     Page Should Contain                   Název ePublikace
#     Page Should Contain                   RIV
#     Fill inputs about ePublication    
#     Fill inputs about Vydani
#     Add Original Files for ePublication   ${VALID_ISBN}
#     Click Button                          form.buttons.save  
#     Page Should Contain                   Položka byla vytvořena

AT02-03 Ohlášení se soubory
    Delete All Test Queues Starting With    ${QUEUE_PREFIX}
    Declare Queue                    aleph  ${QUEUE_NAME}
    Declare Queue Binding            aleph  search     ${QUEUE_NAME}   request
    Declare Queue Binding            aleph  count      ${QUEUE_NAME}   request
    Declare Queue Binding            aleph  validate   ${QUEUE_NAME}   request
    Declare Queue Binding            aleph  export   ${QUEUE_NAME}   request
    Declare Queue                    antivirus  ${QUEUE_NAME}
    Declare Queue Binding            antivirus  antivirus   ${QUEUE_NAME}  request
    #Stop Aleph Daemon
    #Stop Antivirus Daemon
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
    Page Should Contain                   Processing
    Respond as ISBN Validation Daemon     ${VALID_ISBN}  True
    Respond as Aleph Count Daemon         ${VALID_ISBN}  0
    Respond as Antivirus Daemon
    Respond as Aleph Export Daemon        ${VALID_ISBN}
    Submit SysNumber Search at Aleph
    Respond as Aleph Search Daemon        ${VALID_BUT_DUPLICIT_ISBN}
    Sleep   1s
    Pause

AT02-04 Ohlášení se soubory - zpracování chyby z Alephu
    Delete All Test Queues Starting With    ${QUEUE_PREFIX}
    Declare Queue                    aleph  ${QUEUE_NAME}
    Declare Queue Binding            aleph  search     ${QUEUE_NAME}   request
    Declare Queue Binding            aleph  count      ${QUEUE_NAME}   request
    Declare Queue Binding            aleph  validate   ${QUEUE_NAME}   request
    Declare Queue Binding            aleph  export   ${QUEUE_NAME}   request
    Declare Queue                    antivirus  ${QUEUE_NAME}
    Declare Queue Binding            antivirus  antivirus   ${QUEUE_NAME}  request
    Stop Aleph Daemon
    Stop Antivirus Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Fill inputs about ePublication    
    Fill inputs about Vydani
    Add authors for ePublication          Jan Stavěl
    Add Original Files for ePublication   ${VALID_ENGLISH_ISBN}
    Click Button                          form.buttons.save    
    Page Should Contain                   Položka byla vytvořena
    Location Should Contain               lesni-skolky-ve-zline
    Page Should Contain                   Processing
    Respond as ISBN Validation Daemon     ${VALID_ENGLISH_ISBN}  True
    Respond as Aleph Count Daemon         ${VALID_ENGLISH_ISBN}  0
    Respond as Antivirus Daemon
    Respond as Aleph Export Daemon with Exception        ${VALID_ENGLISH_ISBN}
    Sleep   1s
    Pause

# AT02-04 Ohlášení s RIV kategorií
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Page Should Contain                   Ohlášení ePublikací
#     Page Should Contain                   Ohlášování ePeriodik
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Fill inputs about ePublication    
#     Fill inputs about ePublication    
#     Fill inputs about Vydani
#     Add authors for ePublication          Jan Stavěl
#     Add Original Files for ePublication   ${VALID_ISBN}
#     Fill inputs about RIV    
#     Click Button                          form.buttons.save    
#     Page Should Contain                   Položka byla vytvořena
#     RIV category should be selected

# AT02-05 Nastavení kategorií pro RIV
#     Log in as site owner
#     Click Link                   admin
#     Click Link                   Nastavení portálu
#     Click Link                   css=a[href='${PLONE_URL}/portal_registry']
#     Input Text                   name=q    RIV
#     Click Element                css=input[value="Filter"]
#     Click Link                   edeposit content categoriesForRIV
#     Page Should Contain          Upravit záznam    

# AT02-06 Existuje uživatel pro systémové akce
#     Log in                             system    shoj98Phai9
#     Page Should Contain                Přehledová stránka uživatele system

# AT02-07 Ohlášení a odeslání k akvizici - stav Kontrola ISBN
#     Stop Aleph daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Page Should Contain               Kontrola ISBN
#     Page Should Not Contain           Přidat novou položku
#     Page Should Not Contain           Úpravy
    
# AT02-08 Historie akcí s ePublikací
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Click Link                        Historie
#     Log                               Otevře se okno s historií akcí
    
# AT02-09 Systémové zprávy ePublikace
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Page Should Contain                   Systémové zprávy
#     Click Link                            Systémové zprávy
#     Page Should Contain                   Systémové zprávy

# AT02-10 Ohlášení a odeslání k akvizici - systemový uživatel může informovat o probíhajících akcích
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                        ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                         ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Page Should Contain               Lesní školky ve Zlíně
#     Open Workflow Menu
#     Click Element                     link=Oznámit systémovou akci

# AT02-11 Start Aleph Daemon test
#     Stop Aleph Daemon
#     Sleep   1s
#     ${output}=     Run    ps ax | grep alephdaemon
#     Log        ${output}   WARN
#     Should Not Contain    ${output}   edeposit_amqp_alephdaemon.py
#     Start Aleph Daemon
#     Sleep   1s
#     ${output}=     Run    ps ax | grep alephdaemon
#     Log        ${output}   WARN
#     Should Contain        ${output}   edeposit_amqp_alephdaemon.py
#     Stop Aleph Daemon
#     Sleep   1s
#     ${output}=     Run    ps ax | grep alephdaemon
#     Log        ${output}   WARN
#     Should Not Contain    ${output}   edeposit_amqp_alephdaemon.py

# AT02-12 Jaké typy systémových zpráv systém generuje ve stavu Kontrola ISBN
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Click Link                            Systémové zprávy
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline/system-messages
#     Open add new menu    
#     Click Element                         link=ISBN Count Request
#     Input Text                            css=input[id="form-widgets-IBasic-title"]   Kontrola ISBN
#     Input Text                            css=input[id="form-widgets-isbn"]    fasdfasdfas
#     Click Button                          form.buttons.save  
#     Page Should Contain                   Položka byla vytvořena
#     Click Link                            Systémové zprávy
#     Open add new menu    
#     Click Element                         link=ISBN Validation Request
#     Input Text                            css=input[id="form-widgets-IBasic-title"]   Kontrola duplicity ISBN
#     Input Text                            css=input[id="form-widgets-isbn"]    fasdfasdfas
#     Click Button                          form.buttons.save  
#     Page Should Contain                   Položka byla vytvořena
#     Click Link                            Systémové zprávy
#     Open add new menu    
#     Click Element                         link=ISBN Count Result
#     Input Text                            css=input[id="form-widgets-IBasic-title"]   Kontrola duplicity ISBN
#     Input Text                            css=input[id="form-widgets-isbn"]    fasdfasdfas
#     Input Text                            css=input[id="form-widgets-num_of_records"]    10
#     Click Button                          form.buttons.save  
#     Page Should Contain                   Položka byla vytvořena
#     Click Link                            Systémové zprávy
#     Open add new menu
#     Click Element                         link=ISBN Validation Result
#     Input Text                            css=input[id="form-widgets-IBasic-title"]   Kontrola duplicity ISBN
#     Input Text                            css=input[id="form-widgets-isbn"]    fasdfasdfas
#     Select Checkbox                       css=input[id="form-widgets-is_valid-0"]
#     Click Button                          form.buttons.save  
#     Page Should Contain                   Položka byla vytvořena
#     Click Link                            Systémové zprávy
#     Page Should Contain                   Kontrola ISBN
#     Page Should Contain                   Kontrola duplicity ISBN
#     Page Should Contain                   Zjištění duplicity ISBN
    
# AT02-13 Po odeslání ePublikace k akvizici se objeví systémové zprávy
#     Stop Aleph Daemon
#     Start Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Sleep                                 5s
#     Click Link                            Systémové zprávy
#     Page Should Contain                   Kontrola ISBN:
#     Page Should Contain                   Zjištění duplicity ISBN:
#     Page Should Contain                   Výsledky kontroly ISBN
#     Page Should Contain                   Výsledky dotazu na duplicitu ISBN
#     Stop Aleph Daemon

# AT02-14 Ohlaseni ePublikace - stav Antivirus
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Open Workflow Menu
#     Click Element                         link=Všechna ISBN jsou v pořádku
#     Page Should Contain                   Antivirová kontrola
#     Log out
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Page Should Contain                   Antivirová kontrola
#     Page Should Not Contain               Přidat novou položku
#     Page Should Not Contain               Úpravy

# AT02-15 Ohlaseni ePublikace - stav Antivirus - worfklow akce pro system
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Open Workflow Menu
#     Click Element                         link=Všechna ISBN jsou v pořádku
#     Open Workflow Menu
#     Page Should Contain                   Žádný soubor neobsahuje virus
#     Page Should Contain                   Antivirová kontrola jednoho souboru prošla
#     Page Should Contain                   Antivirová kontrola jednoho souboru neprošla
#     Page Should Contain                   Některý soubor obsahuje virus

# AT02-16 Ohlaseni ePublikace - stav Generovani nahledu
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Open Workflow Menu
#     Click Element                         link=Všechna ISBN jsou v pořádku
#     Open Workflow Menu
#     Click Element                         link=Žádný soubor neobsahuje virus
#     Log out
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Page Should Contain                   Generování náhledů
#     Page Should Not Contain               Přidat novou položku
#     Page Should Not Contain               Úpravy


# AT02-17 Ohlaseni ePublikace - stav Generovani nahledu - workflow akce pro system
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Open Workflow Menu
#     Click Element                         link=Všechna ISBN jsou v pořádku
#     Open Workflow Menu
#     Click Element                         link=Žádný soubor neobsahuje virus
#     Open Workflow Menu
#     Page Should Contain Element           link=Máme všechny náhledy vygenerovány
#     Page Should Contain Element           link=Generování některých náhledů skončilo s chybou
#     Page Should Contain Element           link=Generování jednoho náhledu skončilo s chybou
#     Page Should Contain Element           link=Generování jednoho náhledu proběhlo úspěšně

# AT02-18 Ohlaseni ePublikace - stav Export do Alephu
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Open Workflow Menu
#     Click Element                         link=Všechna ISBN jsou v pořádku
#     Open Workflow Menu
#     Click Element                         link=Žádný soubor neobsahuje virus
#     Open Workflow Menu
#     Click Element                         link=Máme všechny náhledy vygenerovány
#     Log out
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Page Should Contain                   Export do Alephu
#     Page Should Not Contain               Přidat novou položku
#     Page Should Not Contain               Úpravy

# AT02-19 Ohlaseni ePublikace - stav Export do Alephu - systemove akce
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Open Workflow Menu
#     Click Element                         link=Všechna ISBN jsou v pořádku
#     Open Workflow Menu
#     Click Element                         link=Žádný soubor neobsahuje virus
#     Open Workflow Menu
#     Click Element                         link=Máme všechny náhledy vygenerovány
#     Page Should Contain                   Export do Alephu
#     Open Workflow Menu
#     Page Should Contain Element           link=Poslal jsem jeden záznam k exportu do Alephu
#     Page Should Contain Element           link=Export jednoho záznamu do Alephu skončil s chybou
#     Page Should Contain Element           link=Export jednoho záznamu do Alephu proběhl úspěšně
#     Page Should Contain Element           link=Všechny exporty do Alephu proběhly úspěšně
#     Page Should Contain Element           link=Některé exporty do Alephu skončily s chybou

# AT02-20 Ohlaseni ePublikace - Export do Alephu - systemove zpravy
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Open Workflow Menu
#     Click Element                         link=Všechna ISBN jsou v pořádku
#     Open Workflow Menu
#     Click Element                         link=Žádný soubor neobsahuje virus
#     Open Workflow Menu
#     Click Element                         link=Máme všechny náhledy vygenerovány
#     Click Link                            Systémové zprávy
#     Open add new menu    
#     Click Element                         link=Aleph Export Request
#     Input Text                            css=input[id="form-widgets-IBasic-title"]     Zaznam k exportu do Alephu
#     Input Text                            css=input[id="form-widgets-originalFileID"]   inzlin-01-2013-s-nasi-tabinkou.pdf
#     Input Text                            css=input[id="form-widgets-isbn"]             isbn-fadsfaljfa
#     Click Button                          form.buttons.save  
#     Page Should Contain                   Položka byla vytvořena
#     Click Link                            Systémové zprávy
#     Open add new menu
#     Click Element                         link=Aleph Export Result
#     Input Text                            css=input[id="form-widgets-IBasic-title"]   Vysledek exportu do Alephu
#     Input Text                            css=input[id="form-widgets-isbn"]           isbn-fadsfjasd
#     Click Button                          form.buttons.save
#     Page Should Contain                   Položka byla vytvořena

# AT02-21 Ohlaseni ePublikace - stav Čekání na Aleph
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Open Workflow Menu
#     Click Element                         link=Všechna ISBN jsou v pořádku
#     Open Workflow Menu
#     Click Element                         link=Žádný soubor neobsahuje virus
#     Open Workflow Menu
#     Click Element                         link=Máme všechny náhledy vygenerovány
#     Open Workflow Menu
#     Click Element                         link=Všechny exporty do Alephu proběhly úspěšně
#     Log out
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Page Should Contain                   Čekání na Aleph
#     Page Should Not Contain               Přidat novou položku
#     Page Should Not Contain               Úpravy

# AT02-22 Ohlaseni ePublikace - stav Příprava akvizice - systémové akce
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Open Workflow Menu
#     Click Element                         link=Všechna ISBN jsou v pořádku
#     Open Workflow Menu
#     Click Element                         link=Žádný soubor neobsahuje virus
#     Open Workflow Menu
#     Click Element                         link=Máme všechny náhledy vygenerovány
#     Open Workflow Menu
#     Click Element                         link=Všechny exporty do Alephu proběhly úspěšně
#     Click Link                            Systémové zprávy
#     Open add new menu    
#     Click Element                         link=Aleph Search SysNumber Request
#     Input Text                            css=input[id="form-widgets-IBasic-title"]     Zaznam k dohledání SysNumber v Alephu
#     Input Text                            css=input[id="form-widgets-isbn"]           isbn-fadsfjasd
#     Click Button                          form.buttons.save  
#     Page Should Contain                   Položka byla vytvořena

# AT02-23 Ohlášení se soubory - s aktivnim pripojenim do Alephu
#     Open Browser with RabbitMQ
#     Switch Browser      1
#     Start Aleph Daemon
#     Declare Queue                    ${QUEUE_NAME}
#     Declare Queue Binding            search    ${QUEUE_NAME}   *
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Sleep    5s
#     ISBNValidationResult is at RabbitMQ Test Queue
#     CountResult is at RabbitMQ Test Queue
#     Zobrazit historii
#     Historie obsahuje zprávu             Poslal jsem jeden záznam k exportu do Alephu
#     Historie obsahuje zprávu             Export jednoho záznamu do Alephu
#     Stop Aleph Daemon
#     Delete Test Queue

# AT02-24 Ohlášení se soubory - s aktivnim pripojenim do Alephu a zobrazenim chyby z Alephu
#     Start Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory a anglickym ISBN
#     Sleep    5s
#     Zobrazit historii
#     Historie obsahuje zprávu             Poslal jsem jeden záznam k exportu do Alephu
#     Historie obsahuje zprávu             Export jednoho záznamu do Alephu skon?il s chybou
#     Historie obsahuje zprávu             Chyba p?i volání služby Aleph
#     Stop Aleph Daemon

# AT02-25 Ohlášení se soubory - kontrola online isbn kontroly
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Fill inputs about ePublication        
#     Fill inputs about Vydani
#     Add authors for ePublication          Jan Stavěl
#     Add Original Files for ePublication   ${WRONG_ISBN}
#     Page Should Contain                   chyba v isbn
#     Click Button                          form.buttons.cancel
#     Page Should Contain                   Ohlášení bylo přerušeno.
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/add-at-once
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Fill inputs about ePublication        
#     Fill inputs about Vydani
#     Add authors for ePublication          Jan Stavěl
#     Add Original Files for ePublication   ${VALID_BUT_DUPLICIT_ISBN}
#     Page Should Contain                   isbn je už použito. Použijte jíné, nebo nahlašte opravu.


# AT02-26 Ohlaseni ePublikace editorem
#     Click link    Registrovat
#     Wait Until Page Contains    Registrace producenta
#     Fill inputs about producent
#     Click Link				Adresa
#     Fill inputs about address
#     Click Link                          Producent
#     Add one administrator
#     Click Link                          Editor producenta
#     Add one editor
#     Click Button               Registrovat
#     Page Should Contain        Vítejte!
#     Page Should Contain        Vaše uživatelská registrace proběhla.
#     Log In                     ${USER_NAME}      ${USER_PASSWORD}
#     Page Should Contain        Přehledová stránka uživatele
#     Click Link                 Ohlášení ePublikací
#     Page Should Contain        Přidat E-Deposit - ePublikace
#     Log out
#     Log In                     ${EDITOR1_NAME}   ${EDITOR1_PASSWORD}
#     Page Should Contain        Přehledová stránka uživatele
#     Click Link                 Ohlášení ePublikací
#     Page Should Contain        Přidat E-Deposit - ePublikace

# AT02-27-00 Ohlaseni ePublikace - balicek pro podporu verzovani je nainstalovany
#     Log in                     ${ADMINISTRATOR_NAME}   ${ADMINISTRATOR_PASSWORD}
#     Go to                      ${PLONE_URL}/prefs_install_products_form
#     Page Should Contain Element   xpath=//input[@id="edeposit.content" and @name="products:list"]
#     Page Should Contain Element   xpath=//input[@id="plone.app.versioningbehavior" and @name="products:list"]
    
# AT02-27 Ohlaseni ePublikace - Original File obsahuje zaznamy z alephu
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Page Should Contain                   Lesní školky ve Zlíně
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline/inzlin-01-2013-s-nasi-tabinkou.pdf
#     Page Should Contain                   inzlin-01-2013-s-nasi-Tabinkou.pdf
#     Open add new menu    
#     Click Element                         link=Aleph Record
#     Fill Aleph Record
#     Click Button                          form.buttons.save
#     Page Should Contain                   Aleph Record
#     Click Link                            inzlin-01-2013-s-nasi-Tabinkou.pdf
#     Page Should Contain                   Aleph Record
#     Click Link                            Úpravy
#     Click Element                         css=input[value="browse..."]
#     Wait Until Page Contains Element      css=a.contenttype-edeposit-content-alephrecord
#     Click Element                         css=a.contenttype-edeposit-content-alephrecord
#     Wait Until Page Contains Element      css=input.contentTreeAdd
#     Execute Javascript                    jQuery('input.contentTreeAdd').click()
#     Page Should Contain Element           css=input[id="form-widgets-related_aleph_record-0"][checked="checked"]
#     Click Button                          form.buttons.save
#     Wait Until Page Contains              Změny byly uloženy
#     Page Should Contain Element           xpath=//div[@id="formfield-form-widgets-related_aleph_record"]//a[text()="Aleph Record"]
#     Page Should Contain Element           xpath=//div[@id="formfield-form-widgets-IRelatedItems-relatedItems"]//a[text()="Lesní školky ve Zlíně"]    
#     Page Should Contain Element           xpath=//fieldset[@id="folder-listing"]//a[text()="Aleph Record"]

# AT02-28 Ohlášení se soubory a s pridelenim ISBN
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Fill inputs about ePublication    
#     Fill inputs about Vydani
#     Add authors for ePublication          Jan Stavěl
#     Add Original Files for ePublication with ISBN generated
#     Click Button                          form.buttons.save
#     Page Should Contain                   Položka byla vytvořena
#     Location Should Contain               lesni-skolky-ve-zline
#     Page Should Contain                   Přidělení ISBN

# AT02-29 Ohlášení se soubory a s chybou kolem ISBN
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Fill inputs about ePublication    
#     Fill inputs about Vydani
#     Add authors for ePublication          Jan Stavěl
#     Add Original Files for ePublication with ISBN generated
#     Unselect Checkbox                     css=input[id="form-widgets-IOriginalFile-generated_isbn-0"]
#     Click Button                          form.buttons.save
#     Page Should Contain                   Přidat E-Deposit - ePublikace
#     Page Should Contain                   Prosím opravte vyznačené chyby.
#     Page Should Contain                   Buď zadejte ISBN, nebo vyberte - Přiřadit ISBN. V tom případě Vám ISBN přiřadí agentura
#     Select Checkbox                       css=input[id="form-widgets-IOriginalFile-generated_isbn-0"]
#     Input Text                            css=input[id="form-widgets-IOriginalFile-isbn"]  ${VALID_ISBN}
#     Click Button                          form.buttons.save
#     Page Should Contain                   Přidat E-Deposit - ePublikace
#     Page Should Contain                   Prosím opravte vyznačené chyby.    
#     Page Should Contain                   Buď zadejte ISBN, nebo vyberte - Přiřadit ISBN. V tom případě Vám ISBN přiřadí agentura
#     Unselect Checkbox                     css=input[id="form-widgets-IOriginalFile-generated_isbn-0"]
#     Click Button                          form.buttons.save
#     Page Should Contain                   Položka byla vytvořena
#     Location Should Contain               lesni-skolky-ve-zline
#     Page Should Contain                   Kontrola ISBN

# AT02-30 Ohlášení se soubory - sledovani zmen zaznamu v Alephu
#     Stop Aleph Daemon
#     Declare Queue                    ${QUEUE_NAME}
#     Declare Queue Binding            search    ${QUEUE_NAME}   *
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Wait Until Page Contains              Položka byla vytvořena
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     System potvrdi ze                     Všechna ISBN jsou v pořádku
#     System potvrdi ze                     Žádný soubor neobsahuje virus
#     System potvrdi ze                     Máme všechny náhledy vygenerovány
#     System potvrdi ze                     Všechny exporty do Alephu proběhly úspěšně
#     Open Workflow Menu
#     Click Element                         link=Load Aleph Records from Aleph
#     Zobrazit historii
#     Historie obsahuje zprávu              Na?tení záznam? z Alephu pro:
#     ${MSG}=                               Get Message From Queue          ${QUEUE_NAME}
#     Log Dictionary                        ${MSG}   WARN
#     Simulate Aleph Search Response        ${MSG}   ${VALID_ISBN}
#     Click Element                         css=div.close
#     Sleep  1s
#     Pause
#     Click Link                            Zobrazení
#     Wait Until Page Contains               Akvizice
#     Click Link                            inzlin-01-2013-s-nasi-Tabinkou.pdf
#     Wait Until Page Contains              Záznam v Alephu: Derviš :(81754)
#     Page Should Contain Element           xpath=//span[@id="form-widgets-IRelatedItems-relatedItems"]//a[text()="Lesní školky ve Zlíně"]
#     Page Should Contain Element           xpath=//span[@id="form-widgets-related_aleph_record"]//a[text()="Záznam v Alephu: Derviš :(81754)"]

