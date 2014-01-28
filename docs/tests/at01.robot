*** Settings ***

Resource  plone/app/robotframework/selenium.robot

Test Setup  Open browser   ${PLONE_URL}   firefox
Test Teardown  Close all browsers

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Dialogs

*** Keywords ***

Page Should Not Contain Error
    Page Should Not Contain        Litujeme, ale tato stránka neexistuje...

Page Does Not Exist
    Page Should Contain        Litujeme, ale tato stránka neexistuje...

Page Does Exist
    Page Should Not Contain        Litujeme, ale tato stránka neexistuje...
    
*** Test Cases ***

# Domovská stránka
#     Page Should Contain Link    Registrovat
#     Page Should Contain Link    Přihlášení
#     Page Should Contain Link    Smlouva s Národní knihovnou
#     Page Should Contain Element    css=h1
#     Capture Page Screenshot      home-page.png
#     Title Should be   E-Deposit - portál pro ohlašování elektronických publikací
#     Page Should Contain     Vítejte na stránkách E-Deposit

# Bezpečnost složky producentů 
#     Pause Execution
#     Go To                       ${PLONE_URL}/producents
#     Page Does Not Exist    
#     Go To                       ${PLONE_URL}/ePublications-in-declarating
#     Page Does Not Exist    
#     Go To                       ${PLONE_URL}/ePublications-waiting-for-approving 
#     Page Does Not Exist    
#     Go To                       ${PLONE_URL}/ePublications-with-errors
#     Page Does Not Exist    
#     Page Should Not Contain Link    Producenti
#     Page Should Not Contain Link    ePublications in declaring
#     Page Should Not Contain Link    ePublications waiting for preparing of acquisition
#     Page Should Not Contain Link    ePublications with errors
    
# UC01-01 Stažení smlouvy
#     Click link          Smlouva s Národní knihovnou
#     Page Should Not Contain Error

Registrace producenta
    Click link        Registrovat
    Pause Execution    
    Page Should Contain   		Registrace producenta
    Page Should Contain Button   	Registrovat
    Input Text				css=#producent-widgets-home_page   http://www.e-deposit.cz
    Input Text				css=#producent-widgets-location   Praha
    Input Text				css=#producent-widgets-contact   Jan Stavěl
    Click Link				Adresa
    Input Text				css=#form-widgets-street  Pašovice 71
    Input Text 				css=#form-widgets-city  Prakšice
    Input Text    			css=#form-widgets-country  Česká republika
    Click Link                          Default
    Click Button                        Přidat
    Input Text                          css=#producent-widgets-administrators-0-widgets-fullname   Jan Stavěl
    Input Text                          css=#producent-widgets-administrators-0-widgets-email   stavel.jan@gmail.com
    Input Text                          css=#producent-widgets-administrators-0-widgets-home_page   www.nkp.cz

    Input Text                          css=#producent-widgets-administrators-0-widgets-location   Pašovice
    Input Text                          css=#producent-widgets-administrators-0-widgets-phone   773230772
    Input Text                          css=#producent-widgets-administrators-0-widgets-street   Pašovice 71
    Input Text                          css=#producent-widgets-administrators-0-widgets-city   Prakšice
    Input Text                          css=#producent-widgets-administrators-0-widgets-country   Česká republika
    Input Text                          css=#producent-widgets-administrators-0-widgets-username   jans
    Input Text                          css=#producent-widgets-administrators-0-widgets-password   PhiEso7
    Input Text                          css=#producent-widgets-administrators-0-widgets-password_ctl   PhiESo7

    Click Button			Registrovat
    Pause Execution    