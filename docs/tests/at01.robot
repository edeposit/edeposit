*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Test Setup       Open browser and create all folders
Test Teardown    Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs

Resource    my-keywords.robot
Variables   variables.py
        
*** Variables ***
    
*** Keywords ***

*** Test Cases ***

Local roles are available
    Log in as site owner
    Go To                               ${PLONE_URL}/producents/
    Local role is available             Producent Administrator
    Local role is available             Producent Editor

Práce se skupinami uživatelů
    Log in as site owner
    Go To                             ${PLONE_URL}/@@usergroup-groupprefs
    Page Should Contain Element          css=input[name="group_Producent Administrators:list"]
    Page Should Contain Element          css=input[name="group_Testers:list"]
    Page Should Contain Element          css=input[name="group_Producent Editors:list"]

Domovská stránka
     Go to homepage
     Page Should Contain Link    Registrovat
     Page Should Contain Link    Přihlášení
     Page Should Contain Link    Smlouva s Národní knihovnou
     Page Should Contain Element    css=h1
     Capture Page Screenshot      home-page.png
     Title Should be   E-Deposit - portál pro ohlašování elektronických publikací
     Page Should Contain     Vítejte na stránkách E-Deposit

Přidávání producenta pres new contentent menu
    Log In as site owner
    Go to     ${PLONE_URL}/producents/    
    Open add new menu
    ${status} =  Run Keyword And Return Status  Click Link
    ...  css=#plone-contentmenu-factories a.contenttype-edeposit-user-producent
    Run keyword if  ${status} != True  Click Link  edeposit-user-producent
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator
    Click button   name=form.buttons.register
    Page Should Contain   Položka byla vytvořena

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

AT01-01 Registrace producenta bez editora
    Click link        Registrovat
    Page Should Contain   		Registrace producenta
    Page Should Contain Button   	Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator
    Click Button			Registrovat
    Page Should Contain                 Vaše uživatelská registrace proběhla.

AT01-02 Registrace producenta a kontrola administratora
    Registrace producenta
    Page Should Contain                 Vaše uživatelská registrace proběhla.
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Page Should Contain Button          Přihlásit se
    Log in as site owner
    User Should Exist                   ${USER_NAME}
    Click Link                          Členství ve skupinách
    Group Should Be Assigned            Producent Administrators
    Group Should Be Assigned            Producent Editors
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Workflow State Is                   waitingForApproving
    Click Link                          Sdílení
    Local Role is Assigned              ${USER_NAME}   E-Deposit: Producent Administrator
    Local Role is Assigned              ${USER_NAME}   Reader
    Local Role is Assigned              ${USER_NAME}   Editor
    Local Role is Assigned              ${USER_NAME}   Reviewer
    Local Role is Assigned              ${USER_NAME}   Contributor
    Log Out
    Log in                              ${USER_NAME}   ${USER_PASSWORD}
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Location Should Be                  ${PLONE_URL}/producents/${PRODUCENT_ID}
    Sharing tab is available    

AT01-03 Registrace producenta s editorem
    Click link        Registrovat
    Page Should Contain   		Registrace producenta
    Page Should Contain Button   	Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator
    Click Link                          Editor producenta
    Add one editor
    Click Button			Registrovat
    Page Should Contain                 Vaše uživatelská registrace proběhla.

AT01-04 Registrace producenta s editorem a kontrola editora
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
    Log Out
    Log in                              ${EDITOR1_NAME}   ${EDITOR1_PASSWORD}
    Go To                               ${PLONE_URL}/producents/${PRODUCENT_ID}
    Location Should Be                  ${PLONE_URL}/producents/${PRODUCENT_ID}
    Sharing tab is not available    
    User can not edit
    User can not add any content
    User can add ePublication

AT01-05 Registrace producenta s editorem - kontrola povinnych policek, shodnosti hesel
    Click link                          Registrovat
    Page Should Contain   		Registrace producenta
    Page Should Contain Button   	Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-fullname     Jan Stavěl
    Click Button			Registrovat
    Page Should Contain                 Prosím opravte vyznačené chyby.
    Page Should Contain                 Některé položky u editora nejsou vyplněny. Buď vyplňte editorovi všechny položky, nebo je všechny smažte.
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password      ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl    ${USER_PASSWORD}
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-email   stavel.jan@gmail.com
    Click Button			Registrovat
    Page Should Contain                 Prosím opravte vyznačené chyby.
    # Page Should Contain                 css=#form-widgets-IAdministrator-administrator-widgets-password[value=''${USER_PASSWORD}']
    # Page Should Contain                 css=#form-widgets-IAdministrator-administrator-widgets-password_ctl[value='${USER_PASSWORD}']
    Page Should Contain                 Některé položky u editora nejsou vyplněny. Buď vyplňte editorovi všechny položky, nebo je všechny smažte.
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password      ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl    ${USER_PASSWORD}
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-phone   773230772
    Input Text                          css=#form-widgets-IEditor-username   ${EDITOR1_NAME}
    Input Text                          css=#form-widgets-IEditor-password   ${EDITOR1_PASSWORD}
    Click Button			Registrovat
    Page Should Contain                 Prosím opravte vyznačené chyby.
    Page Should Contain                 Některé položky u editora nejsou vyplněny. Buď vyplňte editorovi všechny položky, nebo je všechny smažte.
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password      ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl    ${USER_PASSWORD}
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-password   ${EDITOR1_PASSWORD}
    Input Text                          css=#form-widgets-IEditor-password_ctl   wrongpassword
    Click Button			Registrovat
    Page Should Contain                 Prosím opravte vyznačené chyby.
    Page Should Contain                 U editora se neshodují zadaná hesla. Vyplňte hesla znovu.
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password      ${USER_PASSWORD}
    Input Text                          css=#form-widgets-IAdministrator-administrator-widgets-password_ctl    ${USER_PASSWORD}
    Click Link                          Editor producenta
    Input Text                          css=#form-widgets-IEditor-password       ${EDITOR1_PASSWORD}
    Input Text                          css=#form-widgets-IEditor-password_ctl   ${EDITOR1_PASSWORD}
    Click Button			Registrovat
    Page Should Contain                 Vítejte!
    Page Should Contain                 Vaše uživatelská registrace proběhla.

AT01-06 Kontrola zadaných hesel
    Click link        Registrovat
    Page Should Contain   		Registrace producenta
    Page Should Contain Button   	Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator with wrong passwords
    Click Button			Registrovat
    Page should contain                 Prosím opravte vyznačené chyby.
    Page should contain                 U správce producenta se neshodují zadaná hesla. Vyplňte hesla znovu.
    
AT01-07 Kontrola dostupnosti uzivatelskeho jmena pri jedne registraci
    Registrace producenta
    Click link        Registrovat
    Page Should Contain   		Registrace producenta
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator
    Click Button			Registrovat
    Page should contain                 Prosím opravte vyznačené chyby.
    Page should contain                 Uživatelské jméno u správce producenta je již použito. Vyplňte jiné.
    Add one administrator
    Input Text       css=#form-widgets-IAdministrator-administrator-widgets-username   unique-name
    Click Button			Registrovat
    Wait Until Page Contains            Položka byla vytvořena

AT01-08 Kontrola dostupnosti uzivatelskeho jmena u editoru
    Registrace producenta s editorem
    Click link        Registrovat
    Fill inputs about producent
    Click Link				Adresa
    Fill inputs about address
    Click Link                          Producent
    Add one administrator
    Input Text       css=#form-widgets-IAdministrator-administrator-widgets-username   unique-name
    Click Link                          Editor producenta
    Add one editor
    Click Button			Registrovat
    Page should contain                 Prosím opravte vyznačené chyby.
    Page should contain                 Uživatelské jméno u editora je již obsazené. Vyplňte jiné.
    Add one administrator
    Input Text       css=#form-widgets-IAdministrator-administrator-widgets-username   unique-name
    Click Link                          Editor producenta
    Add one editor
    Input Text                          css=#form-widgets-IEditor-username     unique-editor-name
    Click Button			Registrovat
    Wait Until Page Contains            Položka byla vytvořena

AT01-09 Název producenta v portletech je klikací
     Registrace producenta
     Log in                              ${USER_NAME}   ${USER_PASSWORD}

AT01-10 Přidání nového administrátora k existujícímu producentovi a kontrola dostupnosti uzivatelskeho jmena
    Registrace producenta
    Log in                              ${USER_NAME}   ${USER_PASSWORD}
    Click Link                          ${PRODUCENT_TITLE}
    Click Link                          Administrátoři
    Open add new menu
    Choose a Producent Administrator
    Fill inputs about Obsah       producent administrátor       krátký popisek
    Click Link                    Osobní informace
    Fill inputs about Osobni informace
    Click Link                    Přihlášení
    Fill inputs about Prihlaseni  ${USER_NAME}
    Click Button                  Uložit
    Wait Until Page Contains      Prosím opravte vyznačené chyby.
    Page Should Contain           Uživatelské jméno již existuje. Použijte jiné.
    Click Link                    Přihlášení
    Fill inputs about Prihlaseni   ${NEW_UNIQ_USER_NAME}
    Click Button                  Uložit
    Wait Until Page Contains      Položka byla vytvořena

AT01-11 Přidání nového administrátora k existujícímu producentovi a kontrola hesel
    Registrace producenta
    Log in                              ${USER_NAME}   ${USER_PASSWORD}
    Click Link                          ${PRODUCENT_TITLE}
    Click Link                          Administrátoři
    Open add new menu
    Choose a Producent Administrator
    Fill inputs about Obsah       producent administrátor       krátký popisek
    Click Link                    Osobní informace
    Fill inputs about Osobni informace
    Click Link                    Přihlášení
    Fill inputs about Prihlaseni   ${NEW_UNIQ_USER_NAME}     heslo  jineheslo
    Click Button                  Uložit
    Wait Until Page Contains      Prosím opravte vyznačené chyby.
    Page Should Contain           Hesla se neshodují. Zadejte hesla znovu.
    Click Link                    Přihlášení
    Fill inputs about Prihlaseni   ${NEW_UNIQ_USER_NAME}     heslo   heslo
    Click Button                  Uložit
    Wait Until Page Contains      Položka byla vytvořena

AT01-12 Přidání nového editora k existujícímu producentovi a kontrola dostupnosti uzivatelskeho jmena
    Registrace producenta
    Log in                              ${USER_NAME}   ${USER_PASSWORD}
    Click Link                          ${PRODUCENT_TITLE}
    Click Link                          Editoři
    Open add new menu
    Choose a Producent Editor
    Fill inputs about Obsah       producent editor       krátký popisek
    Click Link                    Osobní informace
    Fill inputs about Osobni informace
    Click Link                    Přihlášení
    Fill inputs about Prihlaseni  ${USER_NAME}
    Click Button                  Uložit
    Wait Until Page Contains      Prosím opravte vyznačené chyby.
    Page Should Contain           Uživatelské jméno již existuje. Použijte jiné.
    Click Link                    Přihlášení
    Fill inputs about Prihlaseni   ${NEW_UNIQ_USER_NAME}
    Click Button                  Uložit
    Wait Until Page Contains      Položka byla vytvořena

AT01-13 Přidání nového editora k existujícímu producentovi a kontrola hesel
    Registrace producenta
    Log in                              ${USER_NAME}   ${USER_PASSWORD}
    Click Link                          ${PRODUCENT_TITLE}
    Click Link                          Editoři
    Open add new menu
    Choose a Producent Editor
    Fill inputs about Obsah       producent editor       krátký popisek
    Click Link                    Osobní informace
    Fill inputs about Osobni informace
    Click Link                    Přihlášení
    Fill inputs about Prihlaseni   ${NEW_UNIQ_USER_NAME}     heslo  jineheslo
    Click Button                  Uložit
    Wait Until Page Contains      Prosím opravte vyznačené chyby.
    Page Should Contain           Hesla se neshodují. Zadejte hesla znovu.
    Click Link                    Přihlášení
    Fill inputs about Prihlaseni   ${NEW_UNIQ_USER_NAME}     heslo   heslo
    Click Button                  Uložit
    Wait Until Page Contains      Položka byla vytvořena
