*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

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
    
${EDITOR1_NAME}        editor1
${EDITOR1_PASSWORD}    PhiEso7
    
${EDITOR2_NAME}        editor2
${EDITOR2_PASSWORD}    PhiEso7
    
${EDITOR3_NAME}        editor3
${EDITOR3_PASSWORD}    PhiEso7
    
*** Keywords ***

*** Test Cases ***

# Local roles are available
#      Log in as site owner
#      Go To                               ${PLONE_URL}/producents/
#      Local role is available             RIV Reviewer

# Práce se skupinami uživatelů
#     Log in as site owner
#     Go To                             ${PLONE_URL}/@@usergroup-groupprefs
#     Page Should Contain Element          css=input[name="group_RIV Reviewers:list"]

# Vytvoření RIV posuzovatele
#     Log in as site owner
#     Go To                             ${PLONE_URL}/@@usergroup-userprefs
#     Click Overlay Button        Přidat nového uživatele
#     Input Text       //input[@id='form.fullname']   Jan Stavel
#     Input Text       //input[@id='form.username']   riv
#     Input Text       //input[@id='form.email']      riv@nkp.cz
#     Input Text       //input[@id='form.password']   afado3
#     Input Text       //input[@id='form.password_ctl']   afado3
#     Select Checkbox  //input[@id='form.groups.8']
#     Click Button     Registrovat

Stránka pro RIV posuzovatele
    Vytvoření RIV posuzovatele
    Log In           riv  afado3
    Page Should Contain    Přehledová stránka uživatele Jan Stavel
    Pause
    
# Přehledová stránka posuzovatele od RIVu
#     Go to user page
#     Page Should Contain Link    ePublikace k posouzení RIVem
#     Pause

# Přidávání producenta pres new contentent menu
#     Log In as site owner
#     Go to     ${PLONE_URL}/producents/    
#     Open add new menu
#     ${status} =  Run Keyword And Return Status  Click Link
#     ...  css=#plone-contentmenu-factories a.contenttype-edeposit-user-producent
#     Run keyword if  ${status} != True  Click Link  edeposit-user-producent
#     Fill inputs about producent
#     Click Link				Adresa
#     Fill inputs about address
#     Click Link                          Producent
#     Add one administrator
#     Click button   name=form.buttons.register
#     Page Should Contain   Položka byla vytvořena

# Bezpečnost složky producentů 
#      Go to homepage
#      Go To                        ${PLONE_URL}/producents
#      Page Should Contain Button   Přihlásit se    
#      Go To                        ${PLONE_URL}/ePublications-in-declarating
#      Page Should Contain Button   Přihlásit se    
#      Go To                       ${PLONE_URL}/ePublications-waiting-for-approving 
#      Page Should Contain Button   Přihlásit se    
#      Go To                       ${PLONE_URL}/ePublications-with-errors
#      Page Should Contain Button   Přihlásit se   
#      Page Should Not Contain Link    Producenti
#      Page Should Not Contain Link    ePublications in declaring
#      Page Should Not Contain Link    ePublications waiting for preparing of acquisition
#      Page Should Not Contain Link    ePublications with errors
    
# UC01-01 Stažení smlouvy
#      Click link          Smlouva s Národní knihovnou
#      Page Should Not Contain Error

# UC01-01 Registrace producenta a kontrola administratora
#     Registrace producenta
#     Page Should Contain                 Vaše uživatelská registrace proběhla.
#     Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
#     Page Should Contain Button          Přihlásit se
#     Log in as site owner
#     User Should Exist                   ${USER_NAME}
#     Pause
#     Click Link                          Členství ve skupinách
#     Group Should Be Assigned            Producent Administrators
#     Group Should Be Assigned            Producent Editors
#     Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
#     Workflow State Is                   waitingForApproving
#     Click Link                          Sdílení
#     Local Role is Assigned              ${USER_NAME}   E-Deposit: Producent Administrator
#     Local Role is Assigned              ${USER_NAME}   Reader
#     Local Role is Assigned              ${USER_NAME}   Editor
#     Local Role is Assigned              ${USER_NAME}   Reviewer
#     Local Role is Assigned              ${USER_NAME}   Contributor
#     Log Out
#     Log in                              ${USER_NAME}   ${USER_PASSWORD}
#     Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
#     Location Should Be                  ${PLONE_URL}/producents/${PRODUCENT_ID}
#     Sharing tab is available    

# UC01-01 Kontrola zadaných hesel
#     Click link        Registrovat
#     Page Should Contain   		Registrace producenta
#     Page Should Contain Button   	Registrovat
#     Fill inputs about producent
#     Click Link				Adresa
#     Fill inputs about address
#     Click Link                          Producent
#     Add one administrator with wrong passwords
#     Pause
#     Click Button			Registrovat
#     Page should contain                 problém v údajích administrátora
#     Page should contain                 hesla se musí shodovat
    
# UC01-01 Kontrola dostupnosti uzivatelskeho jmena pri jedne registraci
#     Click link        Registrovat
#     Page Should Contain   		Registrace producenta
#     Page Should Contain Button   	Registrovat
#     Fill inputs about producent
#     Click Link				Adresa
#     Fill inputs about address
#     Click Link                          Producent
#     Add two administrators with the same username
#     Click Button			Registrovat
#     Pause

# UC01-01 Kontrola dostupnosti uzivatelskeho jmena
#     Registrace producenta
#     Click link        Registrovat
#     Fill inputs about producent
#     Click Link				Adresa
#     Fill inputs about address
#     Click Link                          Producent
#     Add one administrator    
#     Click Button			Registrovat
#     Page Should Contain                 problém v údajích administrátora
#     Page Should Contain                 toto uživatelské jméno je už obsazeno, zvolte jiné

UC01-01 Registrace producenta s editorem a kontrola editora
    Registrace producenta s editorem
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Page Should Contain Button          Přihlásit se
    Log in as site owner
    User Should Exist                   ${EDITOR1_NAME}
    Click Link                          Členství ve skupinách
    Group Should Not Be Assigned        Producent Administrators
    Group Should Be Assigned            Producent Editors
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Click Link                          Sdílení
    Local Role is not Assigned          ${EDITOR1_NAME}  E-Deposit: Producent Administrator
    Local Role is Assigned              ${EDITOR1_NAME}  E-Deposit: Producent Editor
    Local Role is Assigned              ${EDITOR1_NAME}  Reader
    Local Role is not Assigned          ${EDITOR1_NAME}  Editor
    Local Role is not Assigned          ${EDITOR1_NAME}  Reviewer
    Local Role is not Assigned          ${EDITOR1_NAME}  Contributor
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Page Should Contain                 Čeká na schválení
    Pause
    Log Out
    Log in                              ${EDITOR1_NAME}   ${EDITOR1_PASSWORD}
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Location Should Be                  ${PLONE_URL}/producents/${PRODUCENT_ID}
    Sharing tab is not available    
    User can not edit
    User can not add any content
    User can add ePublication

# UC01-01 Název producenta v portletech je klikací
#      Registrace producenta
#      Log in                              ${USER_NAME}   ${USER_PASSWORD}
