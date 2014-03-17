*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  my-keywords.robot
    
Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs

*** Variables ***
    
${USER_NAME}        jans
${USER_PASSWORD}    PhiEso7
${SYSTEM_NAME}        system
${SYSTEM_PASSWORD}    shoj98Phai9
${PRODUCENT_ID}     zlinsky-vydavatel
${PRODUCENT_TITLE}  Zlínsky vydavatel
    
*** Test Cases ***

# UC02-01 Domovská stránka uživatele
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Page Should Contain                   Přehledová stránka uživatele
#     Page Should Contain                   Ohlášení ePublikace, ePeriodika, knihy
#    #     Page Should Contain                   Rozpracované ePublikace
#    #     Page Should Contain                   ePublikace s chybami
#     Page Should Contain                   Vyhledat
#     Page Should Contain                   Zlínsky vydavatel    

# UC02-01 Ohlášení bez souboru bez autoru
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Page Should Not Contain               Obsah
#     Page Should Contain                   ePublikace
#     Page Should Contain                   Název ePublikace
#     Page Should Contain                   RIV
#     Fill inputs about ePublication    
#     Click Button                          form.buttons.save  
#     Page Should Contain                   Položka byla vytvořena

# UC02-01 Ohlášení bez souboru s autorem
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Fill inputs about ePublication    
#     Add authors for ePublication
#     Click Button                          form.buttons.save    
#     Page Should Contain                   Položka byla vytvořena

# UC02-01 Ohlášení se soubory
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Fill inputs about ePublication    
#     Add authors for ePublication
#     Add Original Files for ePublication
#     Click Button                          form.buttons.save    
#     Page Should Contain                   Položka byla vytvořena
#     Location Should Contain               lesni-skolky-ve-zline
#     Page Should Contain                   Zadávání
#     Open Workflow Menu
#     Page Should Contain                   K akvizici

# UC02-01 Ohlášení s RIV kategorií
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Page Should Contain                   Ohlášení ePublikací
#     Page Should Contain                   Ohlášování ePeriodik
#     Click Link                            Ohlášení ePublikací
#     Wait Until Page Contains              Přidat E-Deposit - ePublikace
#     Fill inputs about ePublication    
#     Fill inputs about RIV    
#     Click Button                          form.buttons.save    
#     Page Should Contain                   Položka byla vytvořena
#     RIV category should be selected

# UC02-01 Nastavení kategorií pro RIV
#     Log in as site owner
#     Click Link                   admin
#     Click Link                   Nastavení portálu
#     Click Link                   css=a[href='${PLONE_URL}/portal_registry']
#     Input Text                   name=q    RIV
#     Click Element                css=input[value="Filter"]
#     Click Link                   edeposit content categoriesForRIV
#     Page Should Contain          Upravit záznam    

# UC02-01 Existuje uživatel pro systémové akce
#     Log in                             system    shoj98Phai9
#     Page Should Contain                Přehledová stránka uživatele system

# UC02-01 Ohlášení a odeslání k akvizici - systemový uživatel může informovat o pribíhajících akcích
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Open Workflow Menu
#     Click Element                     link=K akvizici
#     Log out
#     Log in                                ${SYSTEM_NAME}   ${SYSTEM_PASSWORD}
#     Go to                             ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
#     Page Should Contain               Lesní školky ve Zlíně
#     Open Workflow Menu
#     Click Element                     link=ISBN jde ke kontrole

# UC02-01 Ohlášení a odeslání k akvizici
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Open Workflow Menu
#     Click Element                     link=K akvizici
#     Page Should Contain               Kontrola ISBN
#     Page Should Not Contain           Přidat novou položku
#     Pause

# UC02-01 Systémové zprávy ePublikace
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Ohlášení se soubory
#     Page Should Contain                   Systémové zprávy
#     Click Link                            Systémové zprávy
#     Page Should Contain                   Systémové zprávy    

UC02-01 Po odeslání ePublikace k akvizici se objeví systémové zprávy
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Ohlášení se soubory
    Open Workflow Menu
    Click Element                         link=K akvizici
    Click Link                            Systémové zprávy
    Page Should Contain                   Kontrola ISBN:
    Page Should Contain                   Zjištění duplicity ISBN:
