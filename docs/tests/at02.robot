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
${PRODUCENT_ID}     zlinsky-vydavatel
${PRODUCENT_TITLE}  Zlínsky vydavatel
    
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
