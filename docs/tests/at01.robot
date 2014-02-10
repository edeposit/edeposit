*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs

*** Variables ***
    
${USER_NAME}       jans
${USER_PASSWORD}   PhiEso7
    
*** Keywords ***

Open browser and create all folders
    Open browser   ${PLONE_URL}   firefox
    Log in as site owner    
    Create producents folder
    Log Out    
    
Page Should Not Contain Error
    Page Should Not Contain        Litujeme, ale tato stránka neexistuje...

Page Does Not Exist
    Page Should Contain        Litujeme, ale tato stránka neexistuje...

Page Does Exist
    Page Should Not Contain        Litujeme, ale tato stránka neexistuje...

Add Dexterity Content
    [arguments]     ${content_type}   ${title}    
    Go to homepage
    Open add new menu

    ${status} =  Run Keyword And Return Status  Click Link
    ...  css=#plone-contentmenu-factories a.contenttype-${content_type}
    Run keyword if  ${status} != True  Click Link  ${content_type}
    Input Text   form.widgets.IBasic.title  ${title}    
    Click button   name=form.buttons.save
    Page Should Contain  Položka byla vytvořena
    Page should contain  ${title}
    ${location} =  Get Location
    [return]  ${location}

Create producents folder
    Add Dexterity Content         edeposit-user-producentfolder    producents

User Should Exist
    [arguments]   ${username}
    Go to                   ${PLONE_URL}/@@user-information?userid=jans
    Page Should Contain     Osobní informace

Fill inputs about producent
    Input Text				css=#producent-widgets-home_page   http://www.e-deposit.cz
    Input Text				css=#producent-widgets-location   Praha
    Input Text				css=#producent-widgets-contact   Jan Stavěl
    
Fill inputs about address
    Input Text				css=#form-widgets-street  Pašovice 71
    Input Text 				css=#form-widgets-city  Prakšice
    Input Text    			css=#form-widgets-country  Česká republika

Add one administrator    
    Click Button                        Přidat
    Input Text                          css=#producent-widgets-administrators-0-widgets-fullname   Jan Stavěl
    Input Text                          css=#producent-widgets-administrators-0-widgets-email   stavel.jan@gmail.com
    Input Text                          css=#producent-widgets-administrators-0-widgets-home_page   www.nkp.cz

    Input Text                          css=#producent-widgets-administrators-0-widgets-location   Pašovice
    Input Text                          css=#producent-widgets-administrators-0-widgets-phone   773230772
    Input Text                          css=#producent-widgets-administrators-0-widgets-street   Pašovice 71
    Input Text                          css=#producent-widgets-administrators-0-widgets-city   Prakšice
    Input Text                          css=#producent-widgets-administrators-0-widgets-country   Česká republika
    Input Text                          css=#producent-widgets-administrators-0-widgets-username   ${USER_NAME}
    Input Text                          css=#producent-widgets-administrators-0-widgets-password   ${USER_PASSWORD}
    Input Text                          css=#producent-widgets-administrators-0-widgets-password_ctl   ${USER_PASSWORD}

Local role is available
    [arguments]   ${rolename}
    Click Link      Sdílení
    Page Should Contain   ${rolename}    

Sharing tab is available
    Page Should Contain Link    Sdílení

Registrace producenta
    Click link        Registrovat
    Page Should Contain   		Registrace producenta
    Page Should Contain Button   	Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Default
    Add one administrator    
    Click Button			Registrovat

Group Should Be Assigned
    [arguments]   ${GROUPNAME}    
    Page Should Contain Element    xpath=//input[@value="${GROUPNAME}" and @name="delete:list"]

Local Role is Assigned
    [arguments]   ${rolename}
    Page Should Contain Element    xpath=//input[@name='entries.role_${ROLENAME}:records' and @checked='checked']    

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
    Go To                               ${PLONE_URL}/producents/edeposit-user-producent
    Location Should Be                  ${PLONE_URL}/producents/edeposit-user-producent
    Log in as site owner
    User Should Exist                   ${USER_NAME}
    Click Link                          Členství ve skupinách
    Group Should Be Assigned            Producent Administrators
    Group Should Be Assigned            Producent Editors
    Group Should Be Assigned            Producent Contributors
    Go To                               ${PLONE_URL}/producents/edeposit-user-producent
    Click Link                          Sdílení
    Local Role is Assigned              E-Deposit: Producent Administrator
    Log Out
    Log in                              ${USER_NAME}   ${USER_PASSWORD}
    Go To                               ${PLONE_URL}/producents/edeposit-user-producent
    Location Should Be                  ${PLONE_URL}/producents/edeposit-user-producent
    Sharing tab is available    


UC02-02 Ohlášení se soubory
    Registrace producenta
    Log in                                ${USER_NAME}   ${USER_PASSWORD}
    Page Should Contain                   Přehledová stránka uživatele
    Page Should Contain                   Ohlášení ePublikace, ePeriodika, knihy
    # Page Should Contain                   Rozpracované ePublikace
    # Page Should Contain                   ePublikace s chybami
    # Page Should Contain                   Vyhledat
