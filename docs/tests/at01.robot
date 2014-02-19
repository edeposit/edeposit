*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

${PLONE_URL} = http://edeposit-aplikace.nkp.cz

Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs

Resource  my-keywords.robot
    
*** Variables ***
    
${USER_NAME}        jans
${USER_PASSWORD}    PhiEso7
${PRODUCENT_ID}     zlinsky-vydavatel
${PRODUCENT_TITLE}  Zlínsky vydavatel
    
*** Keywords ***

*** Test Cases ***

Local roles are available
    Log in as site owner
    Go To                               ${PLONE_URL}/producents/
    Local role is available             Producent Administrator

Domovská stránka
    Go to homepage
    Page Should Contain Link    Registrovat
    Page Should Contain Link    Přihlášení
    Page Should Contain Link    Smlouva s Národní knihovnou
    Page Should Contain Element    css=h1
    Capture Page Screenshot      home-page.png
    Title Should be   E-Deposit - portál pro ohlašování elektronických publikací
    Page Should Contain     Vítejte na stránkách E-Deposit

Přidávání producenta
    Log In as site owner
    Go to     ${PLONE_URL}/producents/    
    Open add new menu
    ${status} =  Run Keyword And Return Status  Click Link
    ...  css=#plone-contentmenu-factories a.contenttype-edeposit-user-producent
    Run keyword if  ${status} != True  Click Link  edeposit-user-producent
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Obsah
    Add one administrator
    Click button   name=form.buttons.register
    Page Should Contain  Item created
    Page should contain  ${PRODUCENT_TITLe}

Bezpečnost složky producentů 
    Go to homepage
    Go To                        ${PLONE_URL}/producents
    Page Should Contain Button   Přihlásit se    
    Go To                        ${PLONE_URL}/ePublications-in-declarating
    Page Should Contain Button   Přihlásit se    
    Go To                       ${PLONE_URL}/ePublications-waiting-for-approving 
    Page Should Contain Button   Přihlásit se    
    Go To                       ${PLONE_URL}/ePublications-with-errors
    Page Should Contain Button   Přihlásit se   
    Page Should Not Contain Link    Producenti
    Page Should Not Contain Link    ePublications in declaring
    Page Should Not Contain Link    ePublications waiting for preparing of acquisition
    Page Should Not Contain Link    ePublications with errors
    
UC01-01 Stažení smlouvy
    Click link          Smlouva s Národní knihovnou
    Page Should Not Contain Error

UC01-01 Registrace producenta
    Registrace producenta
    Page Should Contain                 Vaše uživatelská registrace proběhla.
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Location Should Be                  ${PLONE_URL}/producents/${PRODUCENT_ID}
    Pause
    Page Should Contain                 Odeslat ke schválení
    Pause
    Log in as site owner
    User Should Exist                   ${USER_NAME}
    Click Link                          Členství ve skupinách
    Group Should Be Assigned            Producent Administrators
    Group Should Be Assigned            Producent Editors
    Group Should Be Assigned            Producent Contributors
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Click Link                          Sdílení
    Local Role is Assigned              E-Deposit: Producent Administrator
    Log Out
    Log in                              ${USER_NAME}   ${USER_PASSWORD}
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Location Should Be                  ${PLONE_URL}/producents/${PRODUCENT_ID}
    Sharing tab is available    
