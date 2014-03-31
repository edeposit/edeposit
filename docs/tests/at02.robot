*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  my-keywords.robot
    
Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs
Library  OperatingSystem
    
*** Variables ***
    
${USER_NAME}        jans
${USER_PASSWORD}    PhiEso7
${SYSTEM_NAME}        system
${SYSTEM_PASSWORD}    shoj98Phai9
${PRODUCENT_ID}     zlinsky-vydavatel
${PRODUCENT_TITLE}  Zlínsky vydavatel
${SYSTEM_USER_PASSWORD}   shoj98Phai9    
${SYSTEM_USER_NAME}   system

*** Test Cases ***

UC02-01 Domovská stránka uživatele
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Page Should Contain                   Přehledová stránka uživatele
    Page Should Contain                   Ohlášení ePublikace, ePeriodika, knihy
   #     Page Should Contain                   Rozpracované ePublikace
   #     Page Should Contain                   ePublikace s chybami
    Page Should Contain                   Vyhledat
    Page Should Contain                   Zlínsky vydavatel    

UC02-01 Ohlášení bez souboru bez autoru
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Page Should Not Contain               Obsah
    Page Should Contain                   ePublikace
    Page Should Contain                   Název ePublikace
    Page Should Contain                   RIV
    Fill inputs about ePublication    
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena

UC02-01 Ohlášení bez souboru s autorem
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Fill inputs about ePublication    
    Add authors for ePublication
    Click Button                          form.buttons.save    
    Page Should Contain                   Položka byla vytvořena

UC02-01 Ohlášení se soubory
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Fill inputs about ePublication    
    Add authors for ePublication
    Add Original Files for ePublication
    Click Button                          form.buttons.save    
    Page Should Contain                   Položka byla vytvořena
    Location Should Contain               lesni-skolky-ve-zline
    Page Should Contain                   Zadávání
    Open Workflow Menu
    Page Should Contain                   K akvizici

UC02-01 Ohlášení s RIV kategorií
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Page Should Contain                   Ohlášení ePublikací
    Page Should Contain                   Ohlášování ePeriodik
    Click Link                            Ohlášení ePublikací
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Fill inputs about ePublication    
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

UC02-01 Ohlášení a odeslání k akvizici - systemový uživatel může informovat o probíhajících akcích
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Open Workflow Menu
    Click Element                     link=K akvizici
    Log out
    Log in                        ${SYSTEM_NAME}   ${SYSTEM_PASSWORD}
    Go to                         ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Page Should Contain               Lesní školky ve Zlíně
    Open Workflow Menu
    Click Element                     link=ISBN jde ke kontrole

UC02-01 Ohlášení a odeslání k akvizici - stav Kontrola ISBN
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Open Workflow Menu
    Click Element                     link=K akvizici
    Page Should Contain               Kontrola ISBN
    Page Should Not Contain           Přidat novou položku
    Page Should Not Contain           Úpravy
    
UC02-01 Historie akcí s ePublikací
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Open Workflow Menu
    Click Element                     link=K akvizici
    Click Link                        Historie
    Log                               Otevře se okno s historií akcí
    
UC02-01 Systémové zprávy ePublikace
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Page Should Contain                   Systémové zprávy
    Click Link                            Systémové zprávy
    Page Should Contain                   Systémové zprávy

UC02-01 Jaké typy systémových zpráv systém generuje
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
    Start Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Open Workflow Menu
    Click Element                         link=K akvizici
    Click Link                            Systémové zprávy
    Page Should Contain                   Kontrola ISBN:
    Page Should Contain                   Zjištění duplicity ISBN:
    Sleep                                 2s
    Page Should Contain                   Výsledky kontroly ISBN
    Page Should Contain                   Výsledky dotazu na duplicitu ISBN
    Stop Aleph Daemon


UC02-01 Ohlaseni ePublikace - stav Antivirus
    Stop Aleph Daemon
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Open Workflow Menu
    Click Element                         link=K akvizici
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Open Workflow Menu
    Click Element                         link=All ISBNs are Valid
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
    Open Workflow Menu
    Click Element                         link=K akvizici
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
    Open Workflow Menu
    Click Element                         link=K akvizici
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
    Open Workflow Menu
    Click Element                         link=K akvizici
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
    Open Workflow Menu
    Click Element                         link=K akvizici
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
    Open Workflow Menu
    Click Element                         link=K akvizici
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
    Open Workflow Menu
    Click Element                         link=K akvizici
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
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena
    Pause
    Click Link                            Systémové zprávy
    Open add new menu
    Click Link                            Systémové zprávy
    Open add new menu
    Click Element                         link=Aleph Export Result
    Input Text                            css=#form-widgets-IBasic-title   Vysledek exportu do Alephu
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena
    Click Link                            Systémové zprávy
