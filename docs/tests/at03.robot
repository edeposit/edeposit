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

*** Keywords ***

*** Test Cases ***

Role pro systémového uživatele
    Log in as site owner
    Go To                                ${PLONE_URL}/@@usergroup-groupprefs
    Page Should Contain Element          css=input[name="group_System Users:list"]
    Page Should Contain Element          xpath=//input[@name="group_System Users:list" and @value="E-Deposit: System" and @checked="checked"]

Existuje systemovy uzivatel a je ve spravne skupine
    Log in as site owner
    Go To                                ${PLONE_URL}/@@usergroup-groupprefs
    Click Link                           Uživatelé
    Click Element                        css=a[title="system"]
    Click Link                           Členství ve skupinách
    Page Should Contain Element          xpath=//input[@name="delete:list" and @value="System Users"]
    
Local roles are available
    Log in as site owner
    Go To                               ${PLONE_URL}/producents/
    Local role is available             Acquisitor

Práce se skupinami uživatelů
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-groupprefs
    Page Should Contain Element          css=input[name="group_Acquisitors:list"]

Vytvoření Akvizitora
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-userprefs
    Click Overlay Button        Přidat nového uživatele
    Input Text       //input[@id='form.fullname']   Jan Stavel
    Input Text       //input[@id='form.username']   ${AKVIZITOR_NAME}
    Input Text       //input[@id='form.email']      ${AKVIZITOR_NAME}@nkp.cz
    Input Text       //input[@id='form.password']   ${AKVIZITOR_PASSWORD}
    Input Text       //input[@id='form.password_ctl']   ${AKVIZITOR_PASSWORD}
    Select Checkbox  //input[@id='form.groups.2']
    Click Button     Registrovat
    Page Should Contain    Přehled uživatelů
    Click Link       Skupiny
    Page Should Contain Element          xpath=//input[@name="group_Acquisitors:list" and @value="E-Deposit: Acquisitor" and @checked="checked"]
    
Přehledová stránka pro akvizitora
    Vytvoření Akvizitora
    Log In           ${AKVIZITOR_NAME}   ${AKVIZITOR_PASSWORD}
    Page Should Contain         Přehledová stránka uživatele Jan Stavel

Ohlaseni ePublikace - Akvizice - Prehledova stranka
    Stop Aleph Daemon
    Vytvoření akvizitora
    Log out
    Go To                             ${PLONE_URL}
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
    Open Workflow Menu
    Click Element                         link=Všechny exporty do Alephu proběhly úspěšně
    Open Workflow Menu
    Click Element                         link=Máme všechny sysNumbers z Alephu
    Open Workflow Menu
    Click Element                         link=Dokončit přípravu akvizice
    Log Out
    Log in                                ${AKVIZITOR_NAME}   ${AKVIZITOR_PASSWORD}
    Go to                                 ${PLONE_URL}/producents/${PRODUCENT_ID}/epublications/lesni-skolky-ve-zline
    Page Should Contain                   Lesní školky ve Zlíně
    Go to                                 ${PLONE_URL}/dashboard
    Page Should Contain                   Žádosti o zveřejnění
    Page Should Contain                   Lesní školky ve Zlíně

AT03-07 Pracovní prostředí pracovníka ISBN agentury
    Vytvoření pracovníka ISBN Agentury
    Log out
    Log In      ${ISBN_AGENCY_USER}    ${ISBN_AGENCY_PASSWORD}
    Existuje portlet  Přidělování ISBN
    Existuje portlet  Prehled originalu pro prideleni ISBN    
    Click Element     css=#portal-logo
    Existuje portlet  Přidělování ISBN
    Page Should Contain Link   přehled originálů
    Existuje portlet  Věcná kontrola ISBN

# (run-as-test "../../bin/pybot  -E star:+ -t AT03-08+ at03.robot")
AT03-08 Pracovní prostředí administratora akvizice
    Vytvoření akvizitora   #akvizitor je zaroven i spravce akvizice
    Log Out    
    Log In      ${AKVIZITOR_NAME}    ${AKVIZITOR_PASSWORD}
    Page Should Contain     Přehledová stránka uživatele
    Existuje portlet Cekame na Aleph
    Existuje portlet Originaly co cekají na Aleph
    Click Element   css=#portal-logo
    Existuje portlet Cekame na Aleph

# (run-as-test "../../bin/pybot  -E star:+ -t AT03-09+ at03.robot")
AT03-09 Pracovni prostredi akvizitora
    Vytvoření akvizitora   #akvizitor je zaroven i spravce akvizice
    Log Out    
    Log In      ${AKVIZITOR_NAME}    ${AKVIZITOR_PASSWORD}
    Page Should Contain     Přehledová stránka uživatele
    Existuje portlet Cekame na Aleph
    Existuje portlet Originaly co cekají na Aleph
    Click Element   css=#portal-logo
    Existuje portlet Cekame na Aleph

AT03-10 Přidělení ISBN agenturou
    Vytvoření pracovníka ISBN Agentury
    Log out
    Log In      ${ISBN_AGENCY_USER}    ${ISBN_AGENCY_PASSWORD}
    Click Element    css=#portal-logo
    Click link       přehled originálů
    Klik na nějakou linku s originálem
    Vyplnit ISBN
    Click button     Přiřadit ISBN

AT03-11 Věcná kontrola ISBN
    Vytvoření pracovníka ISBN Agentury
    Otevřít email s přehledem originálů ke kontrole
    Klik na jeden original v emailu
    Log In      ${ISBN_AGENCY_USER}    ${ISBN_AGENCY_PASSWORD}
    V Alephu potvrdit kontrolu ISBN
    eDeposit sleduje zmeny v Alephu
    

AT03-12 Kontrola metadat Akvizicí
    Otevřít email s přehledem originálů ke kontrole akvizicí
    Klik na jeden original v emailu
    Log In      ${AKVIZITOR_NAME}    ${AKVIZITOR_PASSWORD}
    V Alephu potvrdit kontrolu akvizicí
    eDeposit sleduje zmeny v Alephu
    Original se objevi v seznamu pro pripravu katalogizace
