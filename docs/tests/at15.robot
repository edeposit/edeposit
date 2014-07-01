*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  my-keywords.robot

Variables       variables.py
    
Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs
Library  OperatingSystem
    
*** Variables ***

*** Test Cases ***

# UC15-01 Odevzdání dokumentu - kontrola složky pro žádosti a vytvoreni zadosti rucne
#     Stop Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            ${PRODUCENT_TITLE}
#     Click Link                            Odevzdané dokumenty
#     Open add new menu
#     Click Link    css=#plone-contentmenu-factories a.contenttype-edeposit-content-originalfilecontributingrequest
#     Input Text   form.widgets.IBasic.title  odevzdaný dokument
#     Input Text   form.widgets.isbn      ${VALID_BUT_DUPLICIT_ISBN}
#     Click button   name=form.buttons.save
#     Page Should Contain   Položka byla vytvořena
#     Page Should Contain   odevzdaný dokument
#     Open Workflow Menu
#     Click Element                         link=načíst záznamy z Alephu
#     Wait Until Page Contains              čekání na odpověď Alephu
#     Page Should not Contain               Dostali jsme záznamy z Alephu
#     Page Should Not Contain               Přidat novou položku
#     Page Should Not Contain               Úpravy
#     Log out
#     Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/originalfile-contributing/odevzdany-dokument/
#     Open add new menu
#     Click Link    css=#plone-contentmenu-factories a.contenttype-edeposit-content-alephrecord
#     Input Text    form.widgets.IBasic.title        odpoved z Alephu
#     Input Text    form.widgets.isbn                ${VALID_BUT_DUPLICIT_ISBN}
#     Input Text    form.widgets.rok_vydani          2014
#     Input Text    form.widgets.aleph_sys_number    123456
#     Click Button                                   Uložit
#     Wait Until Page Contains                       Položka byla vytvořena
#     Page Should Contain      odpoved z Alephu
#     Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/originalfile-contributing/odevzdany-dokument/
#     Open Workflow Menu
#     Click Element                         link=Dostali jsme záznamy z Alephu

UC15-01 Načtení ePublikace z Alephu a akce systémového uživatele
    Start Aleph daemon
    Registrace producenta
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/
    Open add new menu
    Click Element          css=#edeposit-content-epublication
    Page Should Contain    Přidat E-Deposit - ePublikace
    Fill inputs about ePublication    
    Pause
    
# UC15-01 Odevzdání dokumentu s jednim zaznamem v Alephu
#     Start Aleph Daemon
#     Registrace producenta
#     Log in                                ${USER_NAME}   ${USER_PASSWORD}
#     Click Link                            Odevzdat dokument
#     Page Should Contain Element           css=input#form-widgets-isbn
#     Input Text                            css=input#form-widgets-isbn      ${VALID_BUT_DUPLICIT_ISBN}
#     Click Button                          Načíst záznam z Alephu
#     Page Should Contain                   Žádost na odevzdání dokumentu
#     Open Workflow Menu
#     Click Element                         link=načíst záznamy z Alephu
#     Page Should Contain                   čekání na odpověď Alephu
#     Sleep    4s
#     Click Link                            Zobrazení
#     Wait Until Page Contains              Záznam v Alephu
#     Click Link                            Záznam v Alephu: Derviš :(81754)
#     Wait Until Page Contains              Záznam v Alephu: Derviš :(81754)
#     Click Link                            Žádost na odevzdání dokumentu
#     Wait Until Page Contains              Žádost na odevzdání dokumentu
#     Page Should Not Contain               Přidat novou položku
#     Page Should Not Contain               Úpravy
#     Pause
#     Page Should Contain                   Dostali jsme záznamy z Alephu
#     # Page Should Contain                   Odevzdat dokument
#     # Click Link                            Odevzdat dokument
#     # Page Should Contain                   Odevzdat
#     # Add OriginalFile for ePublication
#     # Click Link                            css=#forms.buttons.save
#     Stop Aleph Daemon

