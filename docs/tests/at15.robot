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
Library  amqp.RabbitMQ

*** Variables ***

*** Test Cases ***

AT15-01 Vytvoreni ePublikace bez dokumentu systemem
    Registrace producenta
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/
    Click Link                            Ohlášení ePublikací
    Open add new menu
    Click Element                         link=E-Deposit - ePublikace
    Wait Until Page Contains              Přidat E-Deposit - ePublikace
    Fill inputs about ePublication    
    Fill inputs about Vydani
    Click Button                          form.buttons.save  
    Page Should Contain                   Položka byla vytvořena
    Open Workflow Menu
    Click Element                         link=Načetl jsem ePublikaci z Alephu
    Page Should Contain                   Zpřístupnění

AT15-02 Odevzdání dokumentu - kontrola složky pro žádosti a vytvoreni zadosti rucne
    Stop Aleph Daemon
    Set Javascript Testing Mode
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            ${PRODUCENT_TITLE}
    Click Link                            Odevzdané dokumenty
    Open add new menu
    Click Link    css=#plone-contentmenu-factories a.contenttype-edeposit-content-originalfilecontributingrequest
    Input Text   form.widgets.IBasic.title  odevzdaný dokument
    Input Text   form.widgets.isbn      ${VALID_BUT_DUPLICIT_ISBN}
    Click button   name=form.buttons.save
    Page Should Contain   Položka byla vytvořena
    Page Should Contain   odevzdaný dokument
    Wait Until Page Contains              čekání na odpověď Alephu
    Page Should not Contain               Dostali jsme záznamy z Alephu
    Page Should Not Contain               Přidat novou položku
    Page Should Not Contain               Úpravy
    Log out
    Log in                                ${SYSTEM_USER_NAME}   ${SYSTEM_USER_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/originalfile-contributing/odevzdany-dokument/
    Open add new menu
    Click Link    css=#plone-contentmenu-factories a.contenttype-edeposit-content-alephrecord
    Input Text    form.widgets.IBasic.title        odpoved z Alephu
    Input Text    form.widgets.isbn                ${VALID_BUT_DUPLICIT_ISBN}
    Input Text    form.widgets.rok_vydani          2014
    Input Text    form.widgets.aleph_sys_number    123456
    Input Text    form.widgets.aleph_library       NKC01
    Click Button                                   Uložit
    Wait Until Page Contains                       Položka byla vytvořena
    Page Should Contain      odpoved z Alephu
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/originalfile-contributing/odevzdany-dokument/
    Open Workflow Menu
    Click Element                         link=Dostali jsme záznamy z Alephu
    Open Workflow Menu
    Click Element                         link=Načetl jsem ePublikaci z Alephu
    Page Should Contain Element           css=#form-widgets-choosen_aleph_record > div > a
    Click Element                         css=#form-widgets-choosen_aleph_record > div > a
    Page Should Contain                   odpoved z Alephu

AT15-03 Odevzdání dokumentu s jednim zaznamem v Alephu
    Start Aleph Daemon
    Set Javascript Testing Mode
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Click Link                            Odevzdat dokument
    Page Should Contain Element           css=input#form-widgets-isbn
    Input Text                            css=input#form-widgets-isbn      ${VALID_BUT_DUPLICIT_ISBN}
    Click Button                          Načíst záznam z Alephu
    Page Should Contain                   Žádost na odevzdání dokumentu
    Page Should Contain                   čekání na odpověď Alephu
    Sleep    5s
    Click Link                            Zobrazení
    Wait Until Page Contains              Záznam v Alephu
    Click Link                            Záznam v Alephu: Derviš :(81754)
    Wait Until Page Contains              Záznam v Alephu: Derviš :(81754)
    Click Link                            Žádost na odevzdání dokumentu
    Wait Until Page Contains              Žádost na odevzdání dokumentu
    Page Should Not Contain               Přidat novou položku
    Page Should Not Contain               Úpravy
    Zobrazit historii
    Historie obsahuje zprávu              Dostali jsme záznamy z Alephu
    Historie obsahuje zprávu              Na?etl jsem ePublikaci z Alephu
    Page Should Contain Element           css=a[href="${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/${EPUBLICATION_ID}"]
    Page Should Contain Element           css=a[href="${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/${EPUBLICATION_ID}/edeposit-content-originalfile"]
    Page Should Contain                   odevzdání dokumentu
    Unset Javascript Testing Mode
    Wait Until Page Contains              Upravit E-Deposit - Soubor s originálem
    Input Text                            css=#form-widgets-url  http://www.grada.cz/book/1000
    Choose File                           css=#form-widgets-file-input  /opt/edeposit/docs/tests/resources/inzlin-01-2013-s-nasi-Tabinkou.pdf
    Select From List by Value             css=#form-widgets-format    PDF
    Click Button                          Uložit    
    Wait Until Page Contains              Změny byly uloženy
    Page Should Contain Element           css=span.summary > a.contenttype-edeposit-content-alephrecord
    Click Link                            Úpravy
    Click Element                         css=input[value="browse..."]
    Choose an Aleph Record
    Page Should Contain Element           css=input[id="form-widgets-related_aleph_record-0"][checked="checked"]
    Click Button                          form.buttons.save
    Wait Until Page Contains              Změny byly uloženy
    Page Should Contain Element           css=#form-widgets-related_aleph_record > div > a
    Stop Aleph Daemon

